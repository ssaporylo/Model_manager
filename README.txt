DjangoREST:
	CREATE MODEL:
		type: POST
		params: name (str), fields('field1,field2')
		endpoint: /create_models/

	UPDATE MODEL:
		type:POST
		params: name(str), fields('field1:value1,field2:value2')
		endpoint: /update_models/

	DELETE MODELE:
		type:POST
		params name(str)
		endpoint: /remove_models/

TECHNOLOGIES:
1. DjangoREST
2. REDIS
3. RabbitMQ
4. Tornado
5. WebSocket

START:
1. In settings.py set credentials for database
2. Create user for Django rest API
3. Start DjangoREST: python manage.py runserver.py
4. Start MessageManager: python MessageManager.py
5. Start Tornado: python Publisher.py
6. Review operation open localhost port 8888
