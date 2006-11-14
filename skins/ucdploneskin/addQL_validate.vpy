qlText = context.REQUEST.get('qlText', None)
qlURL = context.REQUEST.get('qlURL', None)


if not qlText:
  state.setError('qlText', 'Required field', new_status='failure')
else:
  if qlText.find(',') > 0:
    state.setError('qlText', 'The text string must not contain a comma', new_status='failure')

if not qlURL:
  state.setError('qlURL', 'Required field', new_status='failure')


if state.getErrors():
  state.set(portal_status_message='Please correct the errors shown.')

return state


