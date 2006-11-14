deptName = context.REQUEST.get('deptName', None)
address1 = context.REQUEST.get('address1', None)
address2 = context.REQUEST.get('address2', None)
address3 = context.REQUEST.get('address3', None)
address4 = context.REQUEST.get('address4', None)
phone1 = context.REQUEST.get('phone1', None)
phone2 = context.REQUEST.get('phone2', None)
fax1 = context.REQUEST.get('fax1', None)
fax2 = context.REQUEST.get('fax2', None)


if not deptName:
    state.setError('deptName', 'Required field', new_status='failure')

return state
