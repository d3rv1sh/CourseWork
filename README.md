CourseWork
==========

Proxy methods

###auth.getEmployeeToken
Returns auth token for employee by login and password
<pre>
params
  login
  password
return
  token
</pre> 

###employee.getPersonalDetails
Returns personal data of employee by id. If called by employee, id must be equal to id based on token.
<pre>
params
  id
  token
return
  id
  first_name
  last_name
</pre>

###employee.getPaymentMethods
Returns masked card numbers and related ids. Can only be called by employee even not by superuser.
<pre>
params
  id
  token
return
  id
  [method]
    id
    card_number
</pre>
