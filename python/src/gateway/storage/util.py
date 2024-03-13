import pika, json

def upload(f, fs, channel, access):
    # upload file to mongodb server with gridfs
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500

    # Once success then push message in rabbitmq for async comm to video process service 
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        # as exchange is empty routing key is name of queue we are going to use
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # if queue pod crashes or reset, messages should be there
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        # delete file if not processed or added to queue
        fs.delete(fid)
        return "internal server error", 500