/**
 * API Payload Builder Function Node for n8n
 * 
 * This script builds structured API payloads from incoming data.
 * Useful for HTTP Request nodes that need formatted data.
 */

return items.map(item => {
  const data = item.json;
  
  // Build different types of API payloads based on data
  const payload = {
    // Standard fields
    id: data.id || `generated_${Date.now()}`,
    timestamp: new Date().toISOString(),
    source: 'n8n-workflow',
    
    // Dynamic payload based on data type
    ...(data.type === 'user' && {
      user_data: {
        name: data.name,
        email: data.email,
        role: data.role || 'user',
        preferences: {
          notifications: true,
          theme: 'default'
        }
      }
    }),
    
    ...(data.type === 'product' && {
      product_data: {
        name: data.name,
        price: parseFloat(data.price) || 0,
        category: data.category || 'uncategorized',
        in_stock: data.in_stock !== false,
        metadata: {
          created_by: 'n8n',
          tags: data.tags ? data.tags.split(',') : []
        }
      }
    }),
    
    // Default payload for unknown types
    ...(data.type && !['user', 'product'].includes(data.type) && {
      generic_data: {
        type: data.type,
        content: data,
        processed: true
      }
    })
  };
  
  return {
    json: payload
  };
});
