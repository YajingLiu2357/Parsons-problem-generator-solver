import re
import settings
import pymysql.cursors
import uuid
import password_validator
from datetime import date

imgdir = 'img/'

def create_connection():
    """Create a connection to the database."""
    connection = pymysql.connect(host=settings.db_host,
                                 user=settings.db_user,
                                 password=settings.db_password,
                                 db=settings.database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_user(Uname: str, password: str, Email: str, Utype: str, CID: str):
    """ Create a new user

    Args: 
        Uname (str): user name
        Password (str): password
        Email (str): email
        Utype (str): user type (admin, student, teacher)
        CID (str): class id
    
    Returns:
        dict: status(email_exists, success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `User` WHERE `Email`=%s"
                cursor.execute(sql, (Email))
                result = cursor.fetchall()
                if (len(result) != 0):
                    playload['status'] = 'email_exists'
                    return playload
                UID = str(uuid.uuid4())
                if Utype == 'student':
                    result = get_class(CID)
                    if result['status'] == 'error':
                        playload['status'] = 'error'
                        return playload
                    else:
                        sql = "INSERT INTO `User` (`UID`, `Uname`, `HashedPassword`, `Email`, `Utype`, `CID`) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (UID, Uname, password_validator.hash_password(password, UID), Email, Utype, CID))
                else:
                    sql = "INSERT INTO `User` (`UID`, `Uname`, `HashedPassword`, `Email`, `Utype`) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (UID, Uname, password_validator.hash_password(password, UID), Email, Utype))
                connection.commit()
                playload['status'] = 'success'
                playload['uuid'] = UID
                return playload
    except:
        playload['status'] = 'error'
        return playload

def get_user(UID: str):
    """ Get user information

    Args: 
        UID (str): user id
    
    Returns:
        dict: status(success, error), user
    """
    playload = {'status': '', 'user': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `User` WHERE `UID`=%s"
                cursor.execute(sql, (UID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['user'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_user(UID: str, Uname: str, HashedPassword: str, Email: str, Utype: str, CID: str):
    """ Update user information

    Args: 
        UID (str): user id
        Uname (str): user name
        HashedPassword (str): hashed password
        Email (str): email
        Utype (str): user type (admin, student, teacher)
        CID (str): class id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_class(CID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `User` SET `Uname`=%s, `HashedPassword`=%s, `Email`=%s, `Utype`=%s, `CID`=%s WHERE `UID`=%s"
                    cursor.execute(sql, (Uname, HashedPassword, Email, Utype, CID, UID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_user(UID: str):
    """ Delete user

    Args: 
        UID (str): user id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `User` WHERE `UID`=%s"
                cursor.execute(sql, (UID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_class(Cname: str, UID: str):
    """ Create a new class

    Args: 
        Cname (str): class name
        UID (str): user id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_user(UID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Class` (`CID`, `Cname`, `UID`) VALUES (%s, %s, %s)"
                    CID = str(uuid.uuid4())
                    cursor.execute(sql, (CID, Cname, UID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = CID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_class(CID: str):
    """ Get class information

    Args: 
        CID (str): class id
    
    Returns:
        dict: status(success, error), class
    """
    playload = {'status': '', 'class': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Class` WHERE `CID`=%s"
                cursor.execute(sql, (CID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['class'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_class(CID: str, Cname: str, UID: str):
    """ Update class information

    Args: 
        CID (str): class id
        Cname (str): class name
        UID (str): user id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_user(UID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Class` SET `Cname`=%s, `UID`=%s WHERE `CID`=%s"
                    cursor.execute(sql, (Cname, UID, CID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_class(CID: str):
    """ Delete class

    Args: 
        CID (str): class id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Class` WHERE `CID`=%s"
                cursor.execute(sql, (CID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_question(Scope: str, Description: str, PIC: str, Tag: str, SolutionSeq: str, UID: str):
    """ Create a new question
    
    Args:
        Scope (str): question scope
        Description (str): question description
        PIC (str): qustion picture name
        Tag (str): question tag (standard, multiple solutions, insert key code)
        SolutionSeq (str): sequence of subsolutions
        UID (str): user id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_user(UID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Question` (`QID`, `Date`, `Scope`, `Description`, `PIC`, `Tag`, `SolutionSeq`, `UID`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    QID = str(uuid.uuid4())
                    cursor.execute(sql, (QID, date.today().strftime("%Y-%m-%d"), Scope, Description, PIC, Tag, SolutionSeq, UID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = QID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_question(QID: str):
    """ Get question information

    Args: 
        QID (str): question id
    
    Returns:
        dict: status(success, error), question
    """
    playload = {'status': '', 'question': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Question` WHERE `QID`=%s"
                cursor.execute(sql, (QID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['question'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_question(QID: str, Scope: str, Description: str, PIC: str, Tag: str, SolutionSeq: str, UID: str):
    """ Update question information

    Args: 
        QID (str): question id
        Date (date): question generated date
        Scope (str): question scope
        Description (str): question description
        PIC (str): qustion picture name
        Tag (str): question tag (standard, multiple solutions, insert key code)
        SolutionSeq (str): sequence of subsolutions
        UID (str): user id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_user(UID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Question` SET `Scope`=%s, `Description`=%s, `PIC`=%s, `Tag`=%s, `SolutionSeq`=%s, `UID`=%s WHERE `QID`=%s"
                    cursor.execute(sql, (Scope, Description, PIC, Tag, SolutionSeq, UID, QID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_question(QID: str):
    """ Delete question

    Args: 
        QID (str): question id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Question` WHERE `QID`=%s"
                cursor.execute(sql, (QID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_solution(Sname: str, QID: str):
    """ Create a new solution
    
    Args:
        Sname (str): solution name
        QID (str): question id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_question(QID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Solution` (`SID`, `Sname`, `QID`) VALUES (%s, %s, %s)"
                    SID = str(uuid.uuid4())
                    cursor.execute(sql, (SID, Sname, QID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = SID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_solution(SID: str):
    """ Get solution information

    Args: 
        SID (str): solution id
    
    Returns:
        dict: status(success, error), solution
    """
    playload = {'status': '', 'solution': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Solution` WHERE `SID`=%s"
                cursor.execute(sql, (SID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['solution'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_solution(SID: str, Sname: str, QID: str):
    """ Update solution information

    Args: 
        SID (str): solution id
        Sname (str): solution name
        QID (str): question id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_question(QID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Solution` SET `Sname`=%s, `QID`=%s WHERE `SID`=%s"
                    cursor.execute(sql, (Sname, QID, SID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_solution(SID: str):
    """ Delete solution

    Args: 
        SID (str): solution id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Solution` WHERE `SID`=%s"
                cursor.execute(sql, (SID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_block(Tag: str, FragmentSeq: str, DLID: str):
    """ Create a new block
    
    Args:
        Tag (str): block tag (single fragment, multiple fragments))
        FragmentSeq (str): sequence of fragments
        DLID (str): difficulty level id   
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_solution(SID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Block` (`BID`, `Tag`, `FragmentSeq`, `DLID`) VALUES (%s, %s, %s, %s)"
                    BID = str(uuid.uuid4())
                    cursor.execute(sql, (BID, Tag, FragmentSeq, DLID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = BID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_block(BID: str):
    """ Get block information

    Args: 
        BID (str): block id
    
    Returns:
        dict: status(success, error), block
    """
    playload = {'status': '', 'block': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Block` WHERE `BID`=%s"
                cursor.execute(sql, (BID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['block'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_block(BID: str, Tag: str, FragmentSeq: str, DLID: str):
    """ Update block information

    Args: 
        BID (str): block id
        Tag (str): block tag (single fragment, multiple fragments))
        FragmentSeq (str): sequence of fragments
        DLID (str): difficulty level id    
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_difficulty_level(DLID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Block` SET `Tag`=%s, `FragmentSeq`=%s, `DLID`=%s WHERE `BID`=%s"
                    cursor.execute(sql, (Tag, FragmentSeq, DLID, BID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_block(BID: str):
    """ Delete block

    Args: 
        BID (str): block id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Block` WHERE `BID`=%s"
                cursor.execute(sql, (BID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_fragment(Code: str, Tag: str, BID: str):
    """ Create a new fragment
    
    Args:
        Code (str): code
        Tag (str): fragment tag (context, comment))
        BID (str): block id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_block(BID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Fragment` (`FID`, `Code`, `Tag`, `BID`) VALUES (%s, %s, %s, %s)"
                    FID = str(uuid.uuid4())
                    cursor.execute(sql, (FID, Code, Tag, BID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = FID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_fragment(FID: str):
    """ Get fragment information

    Args: 
        FID (str): fragment id
    
    Returns:
        dict: status(success, error), fragment
    """
    playload = {'status': '', 'fragment': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Fragment` WHERE `FID`=%s"
                cursor.execute(sql, (FID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['fragment'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_fragment(FID: str, Code: str, Tag: str, BID: str):
    """ Update fragment information

    Args: 
        FID (str): fragment id
        Code (str): code
        Tag (str): fragment tag (context, comment))
        BID (str): block id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_block(BID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Fragment` SET `Code`=%s, `Tag`=%s, `BID`=%s WHERE `FID`=%s"
                    cursor.execute(sql, (Code, Tag, BID, FID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_fragment(FID: str):
    """ Delete fragment

    Args: 
        FID (str): fragment id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Fragment` WHERE `FID`=%s"
                cursor.execute(sql, (FID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_distractor(Code: str, FID: str):
    """ Create a new distractor
    
    Args:
        Code (str): code
        FID (str): fragment id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_fragment(FID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Distractor` (`DID`, `Code`, `FID`) VALUES (%s, %s, %s)"
                    DID = str(uuid.uuid4())
                    cursor.execute(sql, (DID, Code, FID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = DID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_distractor(DID: str):
    """ Get distractor information

    Args: 
        DID (str): distractor id
    
    Returns:
        dict: status(success, error), distractor
    """
    playload = {'status': '', 'distractor': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Distractor` WHERE `DID`=%s"
                cursor.execute(sql, (DID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['distractor'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_distractor(DID: str, Code: str, FID: str):
    """ Update distractor information

    Args: 
        DID (str): distractor id
        Code (str): code
        FID (str): fragment id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_fragment(FID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Distractor` SET `Code`=%s, `FID`=%s WHERE `DID`=%s"
                    cursor.execute(sql, (Code, FID, DID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_distractor(DID: str):
    """ Delete distractor

    Args: 
        DID (str): distractor id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Distractor` WHERE `DID`=%s"
                cursor.execute(sql, (DID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_feedback(Content: str, DID: str):
    """ Create a new feedback
    
    Args:
        Content (str): content
        DID (str): distractor id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_distractor(DID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Feedback` (`FBID`, `Content`, `DID`) VALUES (%s, %s, %s)"
                    FBID = str(uuid.uuid4())
                    cursor.execute(sql, (FBID, Content, DID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = FBID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_feedback(FBID: str):
    """ Get feedback information

    Args: 
        FBID (str): feedback id
    
    Returns:
        dict: status(success, error), feedback
    """
    playload = {'status': '', 'feedback': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Feedback` WHERE `FBID`=%s"
                cursor.execute(sql, (FBID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['feedback'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_feedback(FBID: str, Content: str, DID: str):
    """ Update feedback information

    Args: 
        FBID (str): feedback id
        Content (str): content
        DID (str): distractor id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_distractor(DID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `Feedback` SET `Content`=%s, `DID`=%s WHERE `FBID`=%s"
                    cursor.execute(sql, (Content, DID, FBID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_feedback(FBID: str):
    """ Delete feedback

    Args: 
        FBID (str): feedback id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Feedback` WHERE `FBID`=%s"
                cursor.execute(sql, (FBID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def create_difficulty_level(DLID: str, Level: str, BlockSeq: str, SID: str):
    """ Create a new difficulty level
    
    Args:
        DLID (str): difficulty level id
        Level (str): level
        BlockSeq (str): block sequence
        SID (str): solution id
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'uuid': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_solution(SID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `DifficultyLevel` (`DLID`, `Level`, `BlockSeq`, `SID`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (DLID, Level, BlockSeq, SID))
                    connection.commit()
                    playload['status'] = 'success'
                    playload['uuid'] = DLID
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def get_difficulty_level(DLID: str):
    """ Get difficulty level information

    Args: 
        DLID (str): difficulty level id
    
    Returns:
        dict: status(success, error), difficulty level
    """
    playload = {'status': '', 'difficulty_level': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `DifficultyLevel` WHERE `DLID`=%s"
                cursor.execute(sql, (DLID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['difficulty_level'] = result[0]
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_difficulty_level(DLID: str, Level: str, BlockSeq: str, SID: str):
    """ Update difficulty level information

    Args: 
        DLID (str): difficulty level id
        Level (str): level
        BlockSeq (str): block sequence
        SID (str): solution id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                result = get_solution(SID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "UPDATE `DifficultyLevel` SET `Level`=%s, `BlockSeq`=%s, `SID`=%s WHERE `DLID`=%s"
                    cursor.execute(sql, (Level, BlockSeq, SID, DLID))
                    connection.commit()
                    playload['status'] = 'success'
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def delete_difficulty_level(DLID: str):
    """ Delete difficulty level

    Args: 
        DLID (str): difficulty level id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `DifficultyLevel` WHERE `DLID`=%s"
                cursor.execute(sql, (DLID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def login_check(email: str, password: str):
    """ Check login information

    Args: 
        email (str): email
        password (str): password
    
    Returns:
        dict: status(success, error), user
    """
    playload = {'status': '', 'user': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `User` WHERE `Email`=%s "
                cursor.execute(sql, (email))
                result = cursor.fetchone()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                given_hashed_password = password_validator.hash_password(password, result['UID'])
                if given_hashed_password == result['HashedPassword']:
                    playload['status'] = 'success'
                    playload['user'] = result
                    return playload
    except:
        playload['status'] = 'error'
        return playload

def create_question_prototype(QName: str, Scope: str, Description: str):
    """ Create a new question prototype
    
    Args:
        QName (str): question name
        Scope (str): scope
        Description (str): description
    
    Returns:
        dict: status(success, error), uuid
    """
    playload=create_question(Scope, Description, '', '', '', '8a9c6766-971f-423a-9d43-f094fc926825')
    print('Success')
    return playload

if __name__ == '__main__':
    res = None
    # res = create_user("YajingLIU", "yajing", "P1908345@mpu.edu.mo", "admin", "")
    # res = create_user("teacher", "teacher", "teacher@mpu.edu.mo", "teacher", "")
    # res = create_class("COMP121", "98b1f434-b934-4b9b-8d41-0d5049a18f1e")
    # res = create_user("student", "student", "student@mpu.edu.mo", "student", "5f8f439d-96bc-48c0-8cc3-45b18cfc35d0")
    # res = create_question("scope", "description", "pic", "tag", "98b1f434-b934-4b9b-8d41-0d5049a18f1e")
    # res = create_solution("solution", "89e69728-21bd-482e-aacf-f1834897c766")
    # res = create_block("9ad6edea-c00e-4adc-a2e8-5caf4a479b20")
    # res = create_fragment("code", "75fac29a-021d-40cd-ad9e-f99e452264c0")
    # res = create_distractor("code", "b26262c2-1449-4bc2-b31f-a73707a10e32")
    # res = create_feedback("content", "03bb3d5b-bc30-4219-b732-f368107317df")
    # res = create_comment("content", "b26262c2-1449-4bc2-b31f-a73707a10e32")
    # res = get_user("44451f2e-5e53-461f-beb2-65c29c7a0cad")
    # res = get_class("5f8f439d-96bc-48c0-8cc3-45b18cfc35d0")
    # res = get_question("89e69728-21bd-482e-aacf-f1834897c766")
    # res = get_solution("9ad6edea-c00e-4adc-a2e8-5caf4a479b20")
    # res = get_block("75fac29a-021d-40cd-ad9e-f99e452264c0")
    # res = get_fragment("b26262c2-1449-4bc2-b31f-a73707a10e32")
    # res = get_distractor("03bb3d5b-bc30-4219-b732-f368107317df")
    # res = get_feedback("27d11e9e-389f-4c03-ae2c-f6c20b3ea0c8")
    # res = get_comment("71ee485a-06cc-42e6-96fe-9a74a57c50a5")
    # res = update_user("44451f2e-5e53-461f-beb2-65c29c7a0cad", "Student", "student", "student@mpu.edu.mo", "student", "5f8f439d-96bc-48c0-8cc3-45b18cfc35d0")
    # res = update_class("5f8f439d-96bc-48c0-8cc3-45b18cfc35d0", "COMP 121", "98b1f434-b934-4b9b-8d41-0d5049a18f1e")
    # res = update_question("89e69728-21bd-482e-aacf-f1834897c766", "Scope", "description", "pic", "tag", "98b1f434-b934-4b9b-8d41-0d5049a18f1e")
    # res = update_solution("9ad6edea-c00e-4adc-a2e8-5caf4a479b20", "Solution", "89e69728-21bd-482e-aacf-f1834897c766")
    # res = update_block("75fac29a-021d-40cd-ad9e-f99e452264c0", "")
    # res = update_fragment("b26262c2-1449-4bc2-b31f-a73707a10e32", "Code", "75fac29a-021d-40cd-ad9e-f99e452264c0")
    # res = update_distractor("03bb3d5b-bc30-4219-b732-f368107317df", "Code", "b26262c2-1449-4bc2-b31f-a73707a10e32")
    # res = update_feedback("27d11e9e-389f-4c03-ae2c-f6c20b3ea0c8", "Content", "03bb3d5b-bc30-4219-b732-f368107317df")
    # res = update_comment("71ee485a-06cc-42e6-96fe-9a74a57c50a5", "Content", "b26262c2-1449-4bc2-b31f-a73707a10e32")
    # res = delete_user("44451f2e-5e53-461f-beb2-65c29c7a0cad")
    # res = delete_class("5f8f439d-96bc-48c0-8cc3-45b18cfc35d0")
    # res = delete_question("89e69728-21bd-482e-aacf-f1834897c766")
    # res = delete_solution("9ad6edea-c00e-4adc-a2e8-5caf4a479b20")
    # res = delete_block("75fac29a-021d-40cd-ad9e-f99e452264c0")
    # res = delete_fragment("b26262c2-1449-4bc2-b31f-a73707a10e32")
    # res = delete_distractor("03bb3d5b-bc30-4219-b732-f368107317df")
    # res = delete_feedback("27d11e9e-389f-4c03-ae2c-f6c20b3ea0c8")
    # res = delete_comment("71ee485a-06cc-42e6-96fe-9a74a57c50a5")
    print(res)