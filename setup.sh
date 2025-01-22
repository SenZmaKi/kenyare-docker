#!/bin/bash

# Create upload directories
mkdir -p uploads/{proposals,audits,quotations}

# Set permissions (using current user's UID/GID)
chmod -R 777 uploads
chown -R $UID:$GID uploads

echo "Upload directories created and permissions set"
