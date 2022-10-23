minikube start
kubectl port-forward --address 0.0.0.0 pod/users-reactions-1-0 5432:5432
>>> conn = psycopg2.connect(dbname="postgres", user="postgres", password="users_reactions_super", host="192.168.56.101")
>>> cur = conn.cursor()
>>> cur.execute("CREATE TABLE user_reaction (id SERIAL, username VARCHAR(20) NOT NULL, reaction VARCHAR(10) NOT NULL, timestamp timestamp(3) without time zone NOT NULL, PRIMARY KEY(id))")
uvicorn reaction_writer.app:app --reload
curl -X POST http://127.0.0.1:8000/analytics/2/aleale/click

