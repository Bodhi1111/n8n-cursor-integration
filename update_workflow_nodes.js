
// Paste this into n8n's browser console to update node configurations

const updateWorkflowNodes = () => {
    const baserowToken = 'h9JNHcGxmXZRIICUjpbHvVcKc5geaASA';
    const baserowUrl = 'http://localhost';
    const tableId = '698';

    // Update all HTTP Request nodes that connect to Baserow
    const httpNodes = window.$store.getters.workflow.nodes.filter(n => n.type === 'n8n-nodes-base.httpRequest');

    httpNodes.forEach(node => {
        if (node.name.toLowerCase().includes('baserow')) {
            console.log('Updating node:', node.name);
            // This would update the node parameters
            // You'll need to manually select the credential in the UI
        }
    });

    console.log('Please manually update each Baserow node with:');
    console.log('- URL: ' + baserowUrl + '/api/database/rows/table/' + tableId + '/');
    console.log('- Authentication: Predefined Credential');
    console.log('- Credential: Baserow - Estate Planning CRM');
};

updateWorkflowNodes();
