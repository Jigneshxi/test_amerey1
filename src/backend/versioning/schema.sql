-- Table to store product data with version control
CREATE TABLE IF NOT EXISTS ProductData (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    -- Add a version column to track changes
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    created_by UUID, -- User who created the record
    updated_by UUID  -- User who last updated the record
);

-- Table to store the audit trail of version changes
CREATE TABLE IF NOT EXISTS ProductDataVersionAudit (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES ProductData(id),
    version INTEGER NOT NULL,
    change_description TEXT,
    changed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    changed_by UUID, -- User who made the change
    old_data JSONB, -- Store the old data as JSON
    new_data JSONB  -- Store the new data as JSON
);