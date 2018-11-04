from datetime import datetime
import calendar
import bson


def get_unix_now():
    """Return current time as unix int
    """

    utc_now = datetime.utcnow()

    unix_now = calendar.timegm(utc_now.utctimetuple())

    return unix_now


def add_inner_document(obj_mongo_coll, str_coll_name):
    """Add empty services collection to all users.\n
    In case of new deployment.

    Parameters
    ----------
    obj_mongo_coll : MongoDB collection object
        Mongo collection for which to add empty collection
    str_coll_name : string
        name of collection to insert
    """

    unix_now = get_unix_now()

    ins_dict = {str_coll_name: [{"uploaded": unix_now}]}

    obj_mongo_coll.update_many({}, {'$set': ins_dict})

    return 1


def add_service_welcome_by_id(obj_mongo_coll, str_serv_name, int_uid):
    """Add empty services collection to all users.\n
    In case of new deployment.

    Parameters
    ----------
    obj_mongo_coll : MongoDB collection object
        Mongo collection for which to add empty collection
    str_serv_name : string
        name of service to insert
    int_uid : int
        user id to add service to
    """

    int_uid = bson.int64.Int64(int_uid)

    unix_now = get_unix_now()

    welcome_dict = {"welcome_msg": {"created": unix_now,
                                    "status": 0}}

    obj_mongo_coll.update({'uid': int_uid}, {"$push": {"services": welcome_dict}})


def chng_service_welcome_status_by_id(obj_mongo_coll, int_uid, int_val):
    """Replaces welcome message service instance for a specific user

    Parameters
    ----------
    obj_mongo_coll : MongoDB collection object
        Mongo collection for which to add empty collection
    int_uid : int
        user id
    int_val : int
        new status value
    """

    int_uid = bson.int64.Int64(int_uid)

    unix_now = get_unix_now()

    welcome_dict = {"welcome_msg": {"created": unix_now,
                                    "status": int_val}}

    obj_mongo_coll.update({"uid": int_uid},
                          {"$pull": {"services": "welcome"}})

    obj_mongo_coll.update({'uid': int_uid}, {"$push": {"services": welcome_dict}})
