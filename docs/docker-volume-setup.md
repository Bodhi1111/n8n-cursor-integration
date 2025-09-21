# Docker Volume Setup for Sales Transcript Processing

## Understanding Docker Volume Mounting

Your Docker container is like a tiny, isolated computer inside your computer. By default, it can't see your desktop files at all. A "volume mount" is you saying: "Hey tiny computer, here's a window into this specific folder on my real computer."

## Current Configuration

Your McAdams Transcripts folder has been mapped as follows:

### Host → Container Mapping
```
"/Users/joshuavaughan/Documents/McAdams Transcripts" → /files/transcripts/incoming
"/Users/joshuavaughan/Documents/McAdams Transcripts/Processed" → /files/transcripts/processed
"/Users/joshuavaughan/Documents/McAdams Transcripts/Archive" → /files/transcripts/archive
```

## What This Means

1. **Inside n8n (container)**: The File Watcher Trigger watches `/files/transcripts/incoming`
2. **On your Mac**: This corresponds to `/Users/joshuavaughan/Documents/McAdams Transcripts`
3. **When you drop a file**: Into your McAdams Transcripts folder, n8n sees it appear in `/files/transcripts/incoming`

## Folder Structure Created

The setup has created this structure for you:

```
/Users/joshuavaughan/Documents/McAdams Transcripts/
├── [New transcript files go here]
├── Processed/     (Files move here after processing)
└── Archive/       (Long-term storage)
```

## Testing the Setup

1. **Start n8n**:
   ```bash
   cd /Users/joshuavaughan/n8n-cursor-integration
   npm run start
   ```

2. **Check the volume mounts**:
   ```bash
   docker exec -it n8n-cursor-integration ls -la /files/transcripts/
   ```
   You should see: `incoming`, `processed`, `archive`

3. **Test file detection**:
   - Create a test file in your McAdams Transcripts folder
   - Check if n8n can see it:
   ```bash
   docker exec -it n8n-cursor-integration ls -la /files/transcripts/incoming/
   ```

## Troubleshooting

### Container Can't See Files
```bash
# Check if mount worked
docker exec -it n8n-cursor-integration ls -la /files/
# Should show: transcripts/

# Check mount details
docker inspect n8n-cursor-integration | grep -A 5 -B 5 Mounts
```

### File Permissions
```bash
# Fix permissions if needed
chmod 755 "/Users/joshuavaughan/Documents/McAdams Transcripts"
chmod 755 "/Users/joshuavaughan/Documents/McAdams Transcripts/Processed"
chmod 755 "/Users/joshuavaughan/Documents/McAdams Transcripts/Archive"
```

### Restart After Volume Changes
```bash
# If you change docker-compose.yml volumes, restart
npm run stop
npm run start
```

## File Naming Convention

For optimal processing, name your transcript files:
```
YYYY-MM-DD_CompanyName_MeetingType.txt
```

Examples:
- `2024-01-15_AcmeCorp_Discovery.txt`
- `2024-01-16_TechStart_Demo.txt`
- `2024-01-17_BigClient_Proposal.txt`

## Workflow Trigger Path

In the n8n workflow, the File Watcher Trigger is configured to watch:
```
/files/transcripts/incoming
```

This is the **container path**, not your Mac path. The volume mount makes this container path mirror your real McAdams Transcripts folder.

## Next Steps

1. ✅ Volume mounts configured
2. ✅ Folder structure created
3. ⏭️ Import the workflow to n8n
4. ⏭️ Configure API credentials
5. ⏭️ Test with a sample transcript

Your transcript processing pipeline is now ready for file system integration!