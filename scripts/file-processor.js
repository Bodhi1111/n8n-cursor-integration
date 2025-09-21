/**
 * File Processor Function Node for n8n
 * 
 * This script processes file data, extracts metadata, and prepares files for further processing.
 * Useful for workflows that handle file uploads or file system operations.
 */

const path = require('path');

return items.map(item => {
  const data = item.json;
  
  // Extract file information
  const fileName = data.fileName || data.name || 'unknown_file';
  const fileSize = data.fileSize || data.size || 0;
  const fileType = data.fileType || data.type || path.extname(fileName);
  const mimeType = data.mimeType || data.mime || 'application/octet-stream';
  
  // Process file metadata
  const fileInfo = {
    // Basic file info
    name: fileName,
    size: fileSize,
    type: fileType,
    mime_type: mimeType,
    
    // Computed fields
    size_mb: Math.round((fileSize / 1024 / 1024) * 100) / 100,
    extension: path.extname(fileName).toLowerCase(),
    basename: path.basename(fileName, path.extname(fileName)),
    directory: path.dirname(fileName),
    
    // Processing status
    processed_at: new Date().toISOString(),
    status: 'ready_for_processing',
    
    // File categorization
    category: getFileCategory(fileType, mimeType),
    is_binary: isBinaryFile(mimeType),
    is_image: mimeType.startsWith('image/'),
    is_document: isDocumentFile(mimeType),
    
    // Original data preserved
    original_data: data
  };
  
  return {
    json: fileInfo
  };
});

// Helper functions
function getFileCategory(extension, mimeType) {
  if (mimeType.startsWith('image/')) return 'image';
  if (mimeType.startsWith('video/')) return 'video';
  if (mimeType.startsWith('audio/')) return 'audio';
  if (mimeType.includes('pdf') || extension === '.pdf') return 'document';
  if (mimeType.includes('text/') || extension === '.txt') return 'text';
  if (mimeType.includes('json') || extension === '.json') return 'data';
  if (mimeType.includes('zip') || extension === '.zip') return 'archive';
  return 'other';
}

function isBinaryFile(mimeType) {
  const binaryTypes = [
    'image/', 'video/', 'audio/', 'application/pdf',
    'application/zip', 'application/octet-stream'
  ];
  return binaryTypes.some(type => mimeType.startsWith(type));
}

function isDocumentFile(mimeType) {
  const documentTypes = [
    'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument',
    'text/plain', 'text/csv'
  ];
  return documentTypes.some(type => mimeType.includes(type));
}
