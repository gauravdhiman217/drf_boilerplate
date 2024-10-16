"""
User role type name
"""

USER_ROLE = ((1, "Admin"), (2, "User"))
ADMIN = 1
USER = 2

"""
User Status 
"""
USER_STATUS = (
    (1, "Active"),
    (2, "Inactive"),
    (3, "Deleted"),
    (4, "Suspended"),
    (5, "Terminated"),
)
ACTIVE = 1
INACTIVE = 2
DELETED = 3
SUSPENDED = 4
TERMINATED = 5

"""
GENDER
"""
GENDER = [("M", "Male"), ("F", "Female"), ("O", "Other")]
MALE = "M"
FEMALE = "F"
OTHER = "O"

"""
Social Logins
"""
SOCIAL_TYPE = ((1, "Google"), (2, "Instagram"), (3, "Facebook"), (4, "Apple"))
GOOGLE = 1
INSTAGRAM = 2
FACEBOOK = 3
APPLE = 4

"""
Device
"""
DEVICE_TYPE = ((1, "Android"), (2, "IOS"))
ANDROID = 1
IOS = 2
