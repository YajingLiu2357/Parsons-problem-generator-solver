import re
import os
import sys
import settings
import pymysql.cursors
import uuid
import password_validator
from datetime import date

fpath = os.path.join(os.path.dirname(__file__))
sys.path.append(fpath)

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

def create_question(Qname: str, Scope: str, Description: str, PIC: str, Type: str, SolutionSeq: str, UID: str):
    """ Create a new question
    
    Args:
        Qname (str): question name
        Scope (str): question scope
        Description (str): question description
        PIC (str): qustion picture name
        Type (str): question types (single solution, multiple solutions, multi-step solutions)
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
                    sql = "INSERT INTO `Question` (`QID`, `Qname`, `Date`, `Scope`, `Description`, `PIC`, `Type`, `SolutionSeq`, `UID`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    QID = str(uuid.uuid4())
                    cursor.execute(sql, (QID, Qname, date.today().strftime("%Y-%m-%d"), Scope, Description, PIC, Type, SolutionSeq, UID))
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

def update_question(QID: str, Qname: str, Scope: str, Description: str, PIC: str, Type: str, SolutionSeq: str, UID: str):
    """ Update question information

    Args: 
        QID (str): question id
        Qname (str): question name
        Scope (str): question scope
        Description (str): question description
        PIC (str): qustion picture name
        Type (str): question types (single solution, multiple solutions, multi-step solutions)
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
                    sql = "UPDATE `Question` SET `QName`=%s, `Scope`=%s, `Description`=%s, `PIC`=%s, `Type`=%s, `SolutionSeq`=%s, `UID`=%s WHERE `QID`=%s"
                    cursor.execute(sql, (Qname, Scope, Description, PIC, Type, SolutionSeq, UID, QID))
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

def create_solution(Sname: str, Type: str, QID: str):
    """ Create a new solution
    
    Args:
        Sname (str): solution file name
        Type (str): solution types (fixed order, not fixed order, insert key code )
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
                    sql = "INSERT INTO `Solution` (`SID`, `Sname`, `Type`, `QID`) VALUES (%s, %s, %s, %s)"
                    SID = str(uuid.uuid4())
                    cursor.execute(sql, (SID, Sname, Type, QID))
                    connection.commit()
                    level = create_difficulty_level('1', '', SID)
                    DLID = level['uuid']
                    cut_solution(Sname, DLID)
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

def update_solution(SID: str, Sname: str, Type: str, QID: str):
    """ Update solution information

    Args: 
        SID (str): solution id
        Sname (str): solution name
        Type (str): solution types (fixed order, not fixed order, insert key code)
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
                    sql = "UPDATE `Solution` SET `Sname`=%s, `Type`=%s, `QID`=%s WHERE `SID`=%s"
                    cursor.execute(sql, (Sname, Type, QID, SID))
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

def create_block(Type: str, FragmentSeq: str, DLID: str):
    """ Create a new block
    
    Args:
        Type (str): block types (single fragment, multiple fragments(context), multiple fragments (unit), multiple fragments (standard)))
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
                result = get_difficulty_level(DLID)
                if result['status'] == 'error':
                    playload['status'] = 'error'
                    return playload
                else:
                    sql = "INSERT INTO `Block` (`BID`, `Type`, `FragmentSeq`, `DLID`) VALUES (%s, %s, %s, %s)"
                    BID = str(uuid.uuid4())
                    cursor.execute(sql, (BID, Type, FragmentSeq, DLID))
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

def update_block(BID: str, Type: str, FragmentSeq: str, DLID: str):
    """ Update block information

    Args: 
        BID (str): block id
        Type (str): block type (single fragment, multiple fragments(context), multiple fragments (unit), multiple fragments (standard))
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
                    playload['status'] = 'error 2'
                    return playload
                else:
                    result = get_block(BID)
                    if result['status'] == 'error':
                        playload['status'] = 'error 3'
                        return playload
                    else:
                        sql = "UPDATE `Block` SET `Type`=%s, `FragmentSeq`=%s, `DLID`=%s WHERE `BID`=%s"
                        cursor.execute(sql, (Type, FragmentSeq, DLID, BID))
                        connection.commit()
                        playload['status'] = 'success'
                        return playload
    except:
        playload['status'] = 'error 1'
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

def create_fragment(Code: str, Type: str, BID: str):
    """ Create a new fragment
    
    Args:
        Code (str): code
        Type (str): fragment types (code, comment))
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
                    sql = "INSERT INTO `Fragment` (`FID`, `Code`, `Type`, `BID`) VALUES (%s, %s, %s, %s)"
                    FID = str(uuid.uuid4())
                    cursor.execute(sql, (FID, Code, Type, BID))
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
                print(playload['fragment'])
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_fragment(FID: str, Code: str, Type: str, BID: str):
    """ Update fragment information

    Args: 
        FID (str): fragment id
        Code (str): code
        Type (str): fragment type (code, comment))
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
                    sql = "UPDATE `Fragment` SET `Code`=%s, `Type`=%s, `BID`=%s WHERE `FID`=%s"
                    cursor.execute(sql, (Code, Type, BID, FID))
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

def create_distractor(Code: str, Reason: str, FID: str):
    """ Create a new distractor
    
    Args:
        Code (str): code
        Reason (str): reason to set this distractor
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
                    sql = "INSERT INTO `Distractor` (`DID`, `Code`, `Reason`, `FID`) VALUES (%s, %s, %s, %s)"
                    DID = str(uuid.uuid4())
                    cursor.execute(sql, (DID, Code, Reason, FID))
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

def update_distractor(DID: str, Code: str, Reason: str, FID: str):
    """ Update distractor information

    Args: 
        DID (str): distractor id
        Code (str): code
        Reason (str): reason to set this distractor
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
                    sql = "UPDATE `Distractor` SET `Code`=%s, `Reason`=%s, `FID`=%s WHERE `DID`=%s"
                    cursor.execute(sql, (Code, Reason, FID, DID))
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

def create_difficulty_level(Level: str, BlockSeq: str, SID: str):
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
                    DLID = str(uuid.uuid4())
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

def create_question_prototype(Qname: str, Scope: str, Description: str, Type: str):
    """ Create a new question prototype
    
    Args:
        Qname (str): question name
        Scope (str): scope
        Description (str): description
    
    Returns:
        dict: status(success, error), uuid
    """
    playload=create_question(Qname, Scope, Description, '', Type, '', '8a9c6766-971f-423a-9d43-f094fc926825')
    return playload

def update_question_solution_seq(QID: str, SolutionSeq: str):
    """ Update question prototype
    
    Args:
        QID (str): question id
        SolutionSeq (str): solution sequence
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `Question` SET `SolutionSeq`=%s WHERE `QID`=%s"
                cursor.execute(sql, (SolutionSeq, QID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_question_type(QID: str, Type: str):
    """ Update question prototype
    
    Args:
        QID (str): question id
        Type (str): type
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `Question` SET `Type`=%s WHERE `QID`=%s"
                cursor.execute(sql, (Type, QID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def upload_solution(files):
    """ Upload solution

    Args: 
        files (file): solution file
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': ''}
    try:
        for file in files:
            path = os.path.join(fpath, 'solution/' + file.filename)
            print(path)
            with open(path, 'wb') as f:
                f.write(file.file.read())
        playload['status'] = 'success'
        return playload
    except:
        playload['status'] = 'error'
        return playload

def cut_solution(fname: str, DLID: str):
    """ Cut solution

    Args: 
        fname (str): file name
    
    Returns:
        dict: status(success, error), uuid
    """
    playload = {'status': '', 'fragments': []}
    try:
        path = os.path.join(fpath, 'solution/' + fname)
        with open(path, 'rb') as f:
            lines = f.readlines()
            for line in lines:
                if not line.isspace():
                    playload['fragments'].append(line.decode('utf-8'))
        print("enter cut_solution")
        create_fragment_prototype(playload['fragments'], DLID)
        playload['status'] = 'success'
        return playload
    except:
        playload['status'] = 'error'
        return playload

def create_fragment_prototype(fragments: list, DLID: str):
    """ Create a new fragment prototype

    Args: 
        fragment (list): fragment
        SID (str): solution id
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        print("enter create_fragment_prototype")
        fragmentSeq = ""
        block = create_block('multiple fragments (standard)', fragmentSeq, DLID)
        for fragment in fragments:
            playload = create_fragment(fragment, '', block['uuid'])
            fragmentSeq += playload['uuid'] + ';'
        print(fragmentSeq)
        playload=update_block(block['uuid'], 'multiple fragments', fragmentSeq, DLID)
        print(playload)
        level = get_difficulty_level(DLID)
        update_difficulty_level(DLID, level['difficulty_level'].Level, block['uuid'], level['difficulty_level'].SID)
        playload['status'] = 'success'
    except:
        playload['status'] = 'error'
        return playload

def get_fragment_prototype(QID: str):
    """ Get fragment prototype

    Args: 
        QID (str): question id
    
    Returns:
        dict: status(success, error), fragments
    """
    playload = {'status': '', 'fragments': []}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                # sql = "SELECT SolutionSeq FROM `Question` WHERE `QID` = %s"
                # cursor.execute(sql, (QID))
                # result = cursor.fetchone()
                # if (result == None):
                #     playload['status'] = 'error'
                #     return playload
                # solutionSeq = result['SolutionSeq']
                # solutionSeq = solutionSeq.split(';')
                # solutionSeq.pop()
                # if (solutionSeq.length == 1):
                #     sql = "SELECT * FROM `Fragment` WHERE `BID` IN (SELECT `BID` FROM `Block` WHERE `DLID` IN (SELECT `DLID` FROM `DifficultyLevel` WHERE `Level` = '1' AND `SID` IN (SELECT `SID` FROM `Solution` WHERE `QID` =%s)))"
                #     cursor.execute(sql, (QID))
                #     result = cursor.fetchall()
                #     if (len(result) == 0):
                #         playload['status'] = 'error'
                #         return playload
                #     playload['status'] = 'success'
                #     playload['fragments'] = result
                #     return playload
                # else:
                    
                # For single solution
                sql = "SELECT * FROM `Fragment` WHERE `BID` IN (SELECT `BID` FROM `Block` WHERE `DLID` IN (SELECT `DLID` FROM `DifficultyLevel` WHERE `Level` = '1' AND `SID` IN (SELECT `SID` FROM `Solution` WHERE `QID` =%s)))"
                cursor.execute(sql, (QID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['fragments'] = result
                return playload
                # For multiple solutions
                # Add if condition to check if the solution is multiple
    except:
        playload['status'] = 'error'
        return playload

def get_sequence_prototype(BID: str):
    """ Get sequence prototype

    Args: 
        BID (str): block id
    
    Returns:
        dict: status(success, error), fragments
    """
    playload = {'status': '', 'sequence': [], 'FID': [], 'FragmentType': []}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT FragmentSeq FROM `Block` WHERE `BID` =%s"
                cursor.execute(sql, (BID))
                result = cursor.fetchone()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload  
                FragmentSeq = result['FragmentSeq']
                FragmentSeq = FragmentSeq.split(';')
                FragmentSeq.pop()
                for fragment in FragmentSeq:
                    playload['FID'].append(fragment)
                    sql = "SELECT * FROM `Fragment` WHERE `FID` =%s"
                    cursor.execute(sql, (fragment))
                    result = cursor.fetchone()
                    playload['sequence'].append(result['Code'])
                    playload['FragmentType'].append(result['Type'])
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_solution_prototype(SID: str, Type: str):
    """ Update solution prototype

    Args: 
        SID (str): solution id
        Type (str): solution type
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `Solution` SET `Type` = %s WHERE `SID` = %s"
                cursor.execute(sql, (Type, SID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def get_distractor_by_fid(FID: str):
    """ Get distractor by fragment id

    Args: 
        FID (str): fragment id
    
    Returns:
        dict: status(success, error), distractors
    """
    playload = {'status': '', 'distractors': []}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Distractor` WHERE `FID` = %s"
                cursor.execute(sql, (FID))
                result = cursor.fetchall()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['distractors'] = result
                return playload
    except:
        playload['status'] = 'error'
        return playload

def update_fragment_type(FID: str, Type: str):
    """ Update fragment type

    Args: 
        FID (str): fragment id
        Type (str): fragment type
    
    Returns:
        dict: status(success, error)
    """
    playload = {'status': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `Fragment` SET `Type` = %s WHERE `FID` = %s"
                cursor.execute(sql, (Type, FID))
                connection.commit()
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def get_fragment_type(FID: str):
    """ Get fragment type

    Args: 
        FID (str): fragment id
    
    Returns:
        dict: status(success, error), type
    """
    playload = {'status': '', 'type': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT Type FROM `Fragment` WHERE `FID` = %s"
                cursor.execute(sql, (FID))
                result = cursor.fetchone()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['type'] = result['Type']
                return playload
    except:
        playload['status'] = 'error'
        return playload

def get_block_multiple_steps(QID: str):
    """ Get block multiple steps

    Args: 
        QID (str): question id
    
    Returns:
        dict: status(success, error), steps
    """
    playload = {'status': '', 'blocks': []}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT BlockSeq FROM `DifficultyLevel` WHERE `Level` = '2' AND `SID` IN (SELECT `SID` FROM `Solution` WHERE `QID` = %s)"
                cursor.execute(sql, (QID))
                result = cursor.fetchone()
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                BlockSeq = result['BlockSeq']
                BlockSeq = BlockSeq.split(';')
                BlockSeq.pop()
                for block in BlockSeq:
                    sql = "SELECT * FROM `Block` WHERE `BID` = %s"
                    cursor.execute(sql, (block))
                    result = cursor.fetchone()
                    playload['blocks'].append(result)
                playload['status'] = 'success'
                return playload
    except:
        playload['status'] = 'error'
        return playload

def get_solution_name(BID: str):
    """ Get solution name

    Args: 
        BID (str): block id
    
    Returns:
        dict: status(success, error), name
    """
    playload = {'status': '', 'Sname': ''}
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT Sname FROM `Solution` WHERE `SID` IN (SELECT SID FROM `DifficultyLevel` WHERE `DLID` IN (SELECT `DLID` FROM `Block` WHERE `BID` = %s))"
                cursor.execute(sql, (BID))
                result = cursor.fetchone()
                print(result)
                if (len(result) == 0):
                    playload['status'] = 'error'
                    return playload
                playload['status'] = 'success'
                playload['Sname'] = result['Sname'].replace('.py', '')
                return playload
    except:
        playload['status'] = 'error'
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
    # res = create_difficulty_level("", "", "7bfaf343-7557-49eb-a9a3-82acf0cafa1b")
    # res = cut_solution("mat2*2.py", "8cc31767-c538-4882-88ac-be9bff127893")
    # res = create_solution("ex.py", "480a1e16-9d9e-44b6-8aa3-48e9d693f19a")
    # res = delete_question("5b7834de-b884-45b6-8239-fba245c5d526")
    # res = get_fragment_prototype("a7210de1-f7a5-4e4f-8307-cafddbdd6550")
    #res = get_fragment("050c0534-d1cd-49bf-91df-7540e568e6c2")
    #get_sequence_prototype("d1048a84-d8dd-44de-8bd2-4f14aaea6aca")
    res = update_block("7a8fdfdf-ac47-48c1-b47e-cca885fd1ad2", "multiple fragments", "de9b5ee1-2e51-4a70-821b-aa543e4d6419;ef9b65c4-7fde-42ea-8ceb-f702265d7368;15ea43cb-2a2d-4140-8e44-900e38f7d2fd;0e85c211-685a-418f-8d10-8328304ea09a;9186012f-97a2-4178-b611-258148912105;21f56142-2611-4a4d-b3e7-d5d7adbb5580;548866bf-19de-48de-87cf-727109863115;", "001c02aa-f1d0-4b55-9218-f8147f50d671")
    res = get_block_multiple_steps("0a0b0d88-24dd-4adb-90e8-bb09e6130dab")
    res = get_solution_name("60b991d7-3603-40fe-bef1-94a55671cd39")
    print(res)