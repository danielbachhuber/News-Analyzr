
# Long descriptions are used generally once per template
def generate_long_description(organization):
    
    org_desc = []
    org_desc.append(organization.name)
    org_desc.append(' is a ' + organization.organization_type.name)
    if organization.address:
        org_desc.append(' located at ' + organization.address)
    org_desc.append('. ')
    if organization.parents.count():
        org_desc.append('It is owned by ')
        for parent in organization.parents.all().select_related():
            org_desc.append('<a href="' + parent.get_absolute_url() + '">' + parent.name + '</a>, ')
        org_desc.append('. ')
    if organization.children.count():
        org_desc.append('It owns ' + str(organization.children.count()) + ' organizations, including ')
        for child in organization.children.all().select_related()[:3]:
            org_desc.append('<a href="' + child.get_absolute_url() + '">' + child.name + '</a>, ')
    return ''.join(org_desc)

# Short descriptions are used in series of organizations    
def generate_short_description(organization):
    org_desc = []
    org_desc.append(organization.organization_type.name)
    if organization.product_set.count() > 0:
        org_desc.append(' with ' +  str(organization.product_set.count()) + ' product(s)' )
    return ''.join(org_desc)

