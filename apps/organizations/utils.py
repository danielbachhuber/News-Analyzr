
def generate_long_description(organization):
    
    org_desc = []
    org_desc.append(organization.name)
    org_desc.append(' is a ' + organization.organization_type.name)
    if organization.address:
        org_desc.append(' located at ' + organization.address)
    org_desc.append('. ')
    if organization.parents.count():
        org_desc.append('It is owned by ')
        for parent in organization.parents.all():
            org_desc.append(parent.name)
        org_desc.append('. ')
    if organization.children.count():
        org_desc.append('It owns ' + str(organization.children.count()) + ' organizations, including ')
        for child in organization.children.all()[:3]:
            org_desc.append('<a href="' + child.get_absolute_url() + '">' + child.name + '</a>, ')
    return ''.join(org_desc)