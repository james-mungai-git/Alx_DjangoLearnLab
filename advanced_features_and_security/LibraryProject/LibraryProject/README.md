# Permissions and Groups Setup

1. Custom Permissions:
   - Book model has custom permissions: can_view, can_create, can_edit, can_delete

2. User Groups:
   - Editors: can create, edit, view
   - Viewers: can only view
   - Admins: full permissions

3. Enforcement:
   - Views use @permission_required('bookshelf.can_edit') etc.
   - Users must belong to groups with appropriate permissions to perform actions.
