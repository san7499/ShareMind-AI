import os
import glob
import uuid
from pathlib import Path

# 1. Import existing services and 2. Use configuration values
from app.config import DOCUMENT_FOLDER
from app.services.parser import document_parser
from app.services.chunker import text_chunker
from app.services.embeddings import embedding_service
from app.services.vectordb import vector_db  # 3. Use singleton vector_db


def main():
    print("🚀 Initializing indexing pipeline...")
    
    # Resolve document path from config
    documents_dir = Path(DOCUMENT_FOLDER)
    
    if not documents_dir.exists():
        print(f"⚠️ Document directory '{documents_dir}' does not exist. Please create it and add documents.")
        return

    # 4. Support PDF, DOCX, TXT via project parser (globbing supported formats)
    supported_extensions = ("*.txt", "*.pdf", "*.docx")
    document_files = []
    for ext in supported_extensions:
        document_files.extend(glob.glob(str(documents_dir / "**" / ext), recursive=True))
    
    if not document_files:
        print(f"⚠️ No supported documents found in {documents_dir}/.")
        return

    # Tracking metrics for summary
    num_documents_processed = 0
    total_chunks_indexed = 0
    num_failed_documents = 0

    print(f"📂 Found {len(document_files)} documents. Starting indexing...")

    # Expected indexing pipeline loop with improvements
    for doc_path in document_files:
        file_path_str = str(doc_path)
        file_name = Path(doc_path).name
        
        try:
            # 4. Parse document using existing project parser (supports PDF, DOCX, TXT)
            text = document_parser.parse(file_path_str)
            if not text or not text.strip():
                print(f"  [Skipped] {file_name} parsed to empty text.")
                num_failed_documents += 1
                continue
                
            # 5. Use metadata from chunker (assumes split returns chunks with rich metadata)
            # Falls back gracefully if chunker returns standard strings vs objects/dictionaries
            chunk_results = text_chunker.split(text, source=file_name)
            
            if not chunk_results:
                print(f"  [Skipped] No chunks generated for {file_name}.")
                num_failed_documents += 1
                continue
                
            # Handle chunk format distinction (if chunker returns text strings vs dicts with metadata)
            chunks = []
            chunk_metadatas = []
            
            for item in chunk_results:
                if isinstance(item, dict):
                    chunks.append(item.get("text", ""))
                    # Merge chunker metadata and ensure source is tracked
                    meta = item.get("metadata", {})
                    meta.setdefault("source", file_name)
                    chunk_metadatas.append(meta)
                else:
                    # Fallback if chunker returns raw text strings
                    chunks.append(item)
                    chunk_metadatas.append({"source": file_name})

            # Generate embeddings
            vectors = embedding_service.embed_batch(chunks)
            
            # 6. Improve IDs (using UUIDs or hash-based combinations to avoid collisions)
            file_hash_base = uuid.uuid5(uuid.NAMESPACE_URL, file_path_str)
            ids = [str(uuid.uuid5(file_hash_base, f"chunk_{i}")) for i in range(len(chunks))]
            
            # Store in VectorDB singleton
            vector_db.add(
                ids=ids,
                embeddings=vectors,
                documents=chunks,
                metadatas=chunk_metadatas
            )
            
            num_documents_processed += 1
            total_chunks_indexed += len(chunks)
            print(f"  [Indexed] {file_name} -> {len(chunks)} chunks")
            
        except Exception as e:
            num_failed_documents += 1
            print(f"❌ Error processing {file_name}: {e}")

    # 7. Summary report
    print("\n" + "="*40)
    print("📊 INDEXING RUN SUMMARY")
    print("="*40)
    print(f"• Number of documents processed : {num_documents_processed}")
    print(f"• Number of chunks indexed      : {total_chunks_indexed}")
    print(f"• Number of failed documents    : {num_failed_documents}")
    print("="*40)

if __name__ == "__main__":
    main()