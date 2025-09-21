/**
 * Conditional Router Function Node for n8n
 * 
 * This script routes items to different outputs based on conditions.
 * Connect multiple outputs to this node to create branching logic.
 */

// Define routing conditions
const routingRules = [
  {
    condition: (data) => data.priority === 'high' || data.urgent === true,
    output: 0, // First output
    label: 'high_priority'
  },
  {
    condition: (data) => data.type === 'notification',
    output: 1, // Second output
    label: 'notifications'
  },
  {
    condition: (data) => data.status === 'error',
    output: 2, // Third output
    label: 'errors'
  },
  {
    condition: (data) => data.processed === true,
    output: 3, // Fourth output
    label: 'processed'
  }
];

// Process each item and determine routing
const routedItems = {
  0: [], // high_priority
  1: [], // notifications
  2: [], // errors
  3: [], // processed
  4: []  // default/fallback
};

items.forEach(item => {
  const data = item.json;
  let routed = false;
  
  // Check each routing rule
  for (const rule of routingRules) {
    if (rule.condition(data)) {
      routedItems[rule.output].push({
        ...item,
        json: {
          ...data,
          _routing_info: {
            routed_to: rule.label,
            timestamp: new Date().toISOString()
          }
        }
      });
      routed = true;
      break;
    }
  }
  
  // Default routing for unmatched items
  if (!routed) {
    routedItems[4].push({
      ...item,
      json: {
        ...data,
        _routing_info: {
          routed_to: 'default',
          timestamp: new Date().toISOString()
        }
      }
    });
  }
});

// Return items for each output (n8n will handle the routing)
// Note: In actual n8n, you would configure multiple outputs and return arrays for each
return [
  routedItems[0], // high_priority
  routedItems[1], // notifications
  routedItems[2], // errors
  routedItems[3], // processed
  routedItems[4]  // default
];
