import sqlite3 as s3

path="music.db"


def create_default():
    file=s3.connect(path)
    f=file.cursor()
    query=f"create table if not exists playlists ([playlist] text,[num_songs] int,[last] int,[loop] text)"
    f.execute(query)
    file.commit()
    file.close()


def valid(data):
    file=s3.connect(path)
    f=file.cursor()
    query=f"select playlist from playlists"
    f.execute(query)
    play=f.fetchall()
    file.commit()
    file.close()
    for i in play:
        if i[0]==data:
            return False
    return True


def add_data(data,name="None",playlist=True):
    file=s3.connect(path)
    f=file.cursor()
    if valid(data[0])==False and playlist:
        return False
    if playlist:
        q1=f'''insert into playlists values("{data[0]}","{0}","{0}","{0}")'''
        q2=f'''create table if not exists "{data[0]}" ([name] text,[path] text,[length] text,[vol] float)'''
        f.execute(q2)
    else:
        q1=f'''insert into "{name}" values("{data[0]}","{data[1]}","{data[2]}","{1}")'''
    f.execute(q1) 
    file.commit()
    file.close()
    return True


def delete_data(data,name=None,playlist=True,table=False):
    file=s3.connect(path)
    f=file.cursor()
    if playlist:
        query1=f'''delete from playlists where playlist="{data}"'''
        query2=f'''drop table {data}'''
    elif table:
        query1=f'''drop table {data}'''
        query2=f'''create able {data} if not exists ([name] text,[path] text,[length] text,[vol] float)'''     
    f.execute(query2)
    f.execute(query1)
    file.commit()
    file.close()

#clear_table("dev")
def read_data(name=None):
    file=s3.connect(path)
    f=file.cursor()
    if name is None:
        q=f'''select playlist,num_songs from playlists'''
    else:
        q=f'''select path from "{name}"'''
    f.execute(q)
    op=f.fetchall()        
    file.commit()
    file.close()
    return op


def update_data(data,name=None,playlist=True):
    file=s3.connect(path)
    f=file.cursor()
    if playlist:
        q=f'''update playlists set playlist="{data[1]}" where playlist={data[0]}'''
    else:
        pass
    file.commit()
    file.close()
    
def clear_table(n):
    file=s3.connect(path)
    f=file.cursor()
    data=read_data(name=n)        
    for i in data:
        q=f'''delete from {n} where name="{i[0]}"'''
        f.execute(q)
        file.commit()
    file.close()

#clear_table("dev")

#add_data("dev")  
#add_data(["s1","s\s\ss",266],name="dev",playlist=False)
#delete_data("dev")     
#delete_data("s1","dev",playlist=False)
#print(read_data())
#create_default()

