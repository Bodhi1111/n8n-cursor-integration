/**
 * Data Processing Function Node for n8n
 * 
 * This script processes incoming data, transforms it, and adds computed fields.
 * Copy this script into an n8n Function node for use in your workflows.
 */

// Process each item in the workflow
return items.map(item => {
  const data = item.json;
  
  // Example data transformations
  const processedData = {
    // Original data
    ...data,
    
    // Add timestamp if not present
    processed_at: data.processed_at || new Date().toISOString(),
    
    // Transform text data
    message: data.message ? data.message.toUpperCase() : '',
    
    // Compute derived fields
    word_count: data.message ? data.message.split(' ').length : 0,
    
    // Add status based on data quality
    status: data.message && data.message.length > 10 ? 'valid' : 'needs_review',
    
    // Hash for deduplication (simple example)
    hash: data.message ? 
      Buffer.from(data.message).toString('base64').slice(0, 8) : 
      'no-message'
  };
  
  return {
    json: processedData
  };
});
