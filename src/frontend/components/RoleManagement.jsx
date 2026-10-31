import React, { useState, useEffect } from 'react';
import { Button, Table, Modal, Form } from 'react-bootstrap';

const RoleManagement = () => {
  const [roles, setRoles] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);

  const [roleName, setRoleName] = useState('');
  const [permissions, setPermissions] = useState([]);

  useEffect(() => {
    // Fetch roles from backend API
    const fetchRoles = async () => {
      try {
        const response = await fetch('/roles'); // Replace with actual API endpoint
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setRoles(data);
      } catch (error) {
        console.error('Failed to fetch roles:', error);
        // Handle error (e.g., display an error message to the user)
      }
    };

    fetchRoles();
  }, []);

  const handleAddRole = () => {
    if (!roleName) {
      alert('Role name is required.');
      return;
    }

    // Validate role name (e.g., no special characters, length limits)

    // Send request to backend to create the role
    fetch('/roles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: roleName, permissions }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setRoles([...roles, data]);
        setShowAddModal(false);
        setRoleName('');
        setPermissions([]);
      })
      .catch(error => {
        console.error('Failed to add role:', error);
        // Handle error (e.g., display an error message to the user)
      });
  };

  const handleEditRole = () => {
    if (!selectedRole) {
      alert('Please select a role to edit.');
      return;
    }

    if (!roleName) {
      alert('Role name is required.');
      return;
    }
    
    // Send request to backend to update the role
    fetch(`/roles/${selectedRole.id}`, { // Replace with actual API endpoint
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: roleName, permissions }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const updatedRoles = roles.map(role => (role.id === selectedRole.id ? data : role));
        setRoles(updatedRoles);
        setShowEditModal(false);
        setSelectedRole(null);
        setRoleName('');
        setPermissions([]);
      })
      .catch(error => {
        console.error('Failed to update role:', error);
        // Handle error (e.g., display an error message to the user)
      });
  };

  const handleDeleteRole = (id) => {
    // Confirm deletion with the user
    if (window.confirm('Are you sure you want to delete this role?')) {
      // Send request to backend to delete the role
      fetch(`/roles/${id}`, { // Replace with actual API endpoint
        method: 'DELETE',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          // Remove the deleted role from the state
          const updatedRoles = roles.filter(role => role.id !== id);
          setRoles(updatedRoles);
        })
        .catch(error => {
          console.error('Failed to delete role:', error);
          // Handle error (e.g., display an error message to the user)
        });
    }
  };
  
  const handleSelectRole = (role) => {
    setSelectedRole(role);
    setRoleName(role.name);
    setPermissions(role.permissions || []);
    setShowEditModal(true);
  };

  return (
    <div>
      <h2>Role Management</h2>

      <Button onClick={() => setShowAddModal(true)}>Add Role</Button>

      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Permissions</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {roles.map(role => (
            <tr key={role.id}>
              <td>{role.id}</td>
              <td>{role.name}</td>
              <td>{role.permissions ? role.permissions.join(', ') : ''}</td>
              <td>
                <Button onClick={() => handleSelectRole(role)}>Edit</Button>
                <Button onClick={() => handleDeleteRole(role.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      <Modal show={showAddModal} onHide={() => setShowAddModal(false)}>
        <Modal.Header>
          <Modal.Title>Add Role</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Role Name</Form.Label>
              <Form.Control type="text" value={roleName} onChange={(e) => setRoleName(e.target.value)} />
            </Form.Group>
            {/* Add permissions input here (e.g., checkboxes) */}
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => setShowAddModal(false)}>Cancel</Button>
          <Button onClick={handleAddRole}>Add</Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
        <Modal.Header>
          <Modal.Title>Edit Role</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Role Name</Form.Label>
              <Form.Control type="text" value={roleName} onChange={(e) => setRoleName(e.target.value)} />
            </Form.Group>
            {/* Add permissions input here (e.g., checkboxes) */}
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => setShowEditModal(false)}>Cancel</Button>
          <Button onClick={handleEditRole}>Update</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default RoleManagement;