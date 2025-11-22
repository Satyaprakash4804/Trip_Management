from db import get_db_connection

class UserModel:

    # ---------------------------------------------------
    # CREATE USER (master creates: username, password, role)
    # ---------------------------------------------------
    @staticmethod
    def create_user(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users 
            (name, mobile, email, college_id, role, username, password,
             selfie, college_id_card, aadhar_student, aadhar_parent,
             health_issue, is_verified)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data.get("name"),
            data.get("mobile"),
            data.get("email"),
            data.get("college_id"),

            data.get("role"),
            data.get("username"),
            data.get("password"),

            data.get("selfie"),
            data.get("college_id_card"),
            data.get("aadhar_student"),
            data.get("aadhar_parent"),

            data.get("health_issue"),
            data.get("is_verified")
        ))
    
        conn.commit()
        cursor.close()
        conn.close()
        return True


    # ---------------------------------------------------
    # GET USER (by username)
    # ---------------------------------------------------
    @staticmethod
    def get_user_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result


    # ---------------------------------------------------
    # COMPLETE REGISTRATION
    # ---------------------------------------------------
    @staticmethod
    def update_registration(user_id, form, files):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET 
                name=%s,
                mobile=%s,
                email=%s,
                college_id=%s,
                selfie=%s,
                college_id_card=%s,
                aadhar_student=%s,
                aadhar_parent=%s,
                health_issue=%s,
                is_verified=1
            WHERE id=%s
        """, (
            form.get("name"),
            form.get("mobile"),
            form.get("email"),
            form.get("college_id"),

            files.get("selfie"),
            files.get("college_id_card"),
            files.get("aadhar_student"),
            files.get("aadhar_parent"),

            form.get("health_issue"),
            user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True, "message": "Registration completed!"}



    # ---------------------------------------------------
    # FETCH ALL STUDENTS WITH FULL DETAILS
    # ---------------------------------------------------
    @staticmethod
    def get_all_students():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, username, name, mobile, email, college_id,selfie, is_verified
            FROM users
            WHERE role='student'
            ORDER BY id DESC
        """)

        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data


    # ---------------------------------------------------
    # FETCH ALL ADMINS WITH FULL DETAILS
    # ---------------------------------------------------
    @staticmethod
    def get_all_admins():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, username, name, mobile, email, college_id,selfie, is_verified
            FROM users
            WHERE role='admin'
            ORDER BY id DESC
        """)

        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data


    # ---------------------------------------------------
    # DELETE USER
    # ---------------------------------------------------
    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True


    @staticmethod
    def update_user_by_master(user_id, data):
        conn = get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute("""
            UPDATE users SET 
                name=%s,
                mobile=%s,
                email=%s,
                college_id=%s
            WHERE id=%s
        """, (
            data.get("name"),
            data.get("mobile"),
            data.get("email"),
            data.get("college_id"),
            user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return True
