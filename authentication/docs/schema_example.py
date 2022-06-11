from drf_yasg import openapi

EMAIL_REGISTRATION_INPUT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "provider_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Provider Type",
            enum=["AI", "DISI", "OEMI"],
        ),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="Provider Email"),
    },
)

PHONE_REGISTRATION_INPUT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "provider_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Provider Type",
            enum=["AI", "DISI", "OEMI"],
        ),
        "phone_number": openapi.Schema(
            type=openapi.TYPE_STRING, description="Provider Phone"
        ),
    },
)

COMPLETE_REGISTRATION_INPUT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="First Name"
        ),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last Name"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="Phone"),
        "avatar": openapi.Schema(type=openapi.TYPE_STRING, description="Avatar url"),
        "city": openapi.Schema(type=openapi.TYPE_STRING, description="City"),
        "state": openapi.Schema(type=openapi.TYPE_STRING, description="State"),
        "country": openapi.Schema(type=openapi.TYPE_STRING, description="Country"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
    },
)

LOGOUT_INPUT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="Access Token"
        )
    },
)

REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "id": "59a6119e771c4aa09fc8276506d3bae5",
            "first_name": "Jesse",
            "last_name": "Bingo",
            "company_name": "Balh Blah Inc",
        }
    }
}

EMAIL_REGISTRATION_EXISITING_USER_RESPONSE = {
    "application/json": {
        "errors": {"email": ["A user has already registered with this email address"]}
    }
}

PHONE_REGISTRATION_EXISITING_USER_RESPONSE = {
    "application/json": {
        "errors": {
            "phone_number": ["A user has already registered with this phone number"]
        }
    }
}


EMAIL_REGISTRATION_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["Enter a valid email address."],
            "provider_type": ["This field is required."],
        }
    }
}

PHONE_REGISTRATION_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "phone_number": ["This field is required."],
            "provider_type": ["This field is required."],
        }
    }
}

COMPLETE_REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "id": "2322f9b3d0774c28904f2ae2dfc197e9",
            "first_name": "Jone",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "phone_number": "+2348064667317",
            "city": "Lekki",
            "state": "Lagos",
            "country": "Nigeria",
        }
    }
}

COMPLETE_REGISTRATION_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["Enter a valid email address."],
            "password": ["password is required"],
        }
    }
}


LOGIN_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "user": {
                "id": "4a62dd1780834c4e83458067e2829cfb",
                "first_name": "Jesse",
                "last_name": "Bingo",
            },
            "token": {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
            },
        }
    }
}

LOGIN_WITH_EMAIL_UNAUTHORISED_RESPONSE = {
    "application/json": {"message": "Email or password is not correct"}
}

LOGIN_WITH_EMAIL_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["This field is required."],
            "password": ["This field is required."],
        }
    }
}

LOGIN_WITH_PHONE_UNAUTHORISED_RESPONSE = {
    "application/json": {"message": "Phone number or password is not correct"}
}

LOGIN_WITH_PHONE_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "phone_number": ["This field is required."],
            "password": ["This field is required."],
        }
    }
}

PASSWORD_RESET_INITIATE_SUCCESS_RESPONSE = {
    "application/json": {"data": {"completed": True, "action": "PASSWORD_RESET"}}
}
PASSWORD_RESET_INITIATE_BAD_INPUT_RESPONSE = {
    "application/json": {"errors": {"email": ["This field is required."]}}
}

PASSWORD_RESET_VALIDATE_SUCCESS_RESPONSE = {
    "application/json": {"data": {"reset_token": "574f8fe2f1b644878fa24ec850e95...."}}
}
PASSWORD_RESET_VALIDATE_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "reset_token": ["This field is required."],
            "reset_code": ["This field is required."],
        }
    }
}
PASSWORD_RESET_FINALIZE_SUCCESS_RESPONSE = {"application/json": {"data": True}}
PASSWORD_RESET_FINALIZE_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "reset_token": ["This field is required."],
            "new_password": ["This field is required."],
        }
    }
}

EMAIL_REGISTRATION_RESPONSES = {
    201: openapi.Response(
        description="Created User", examples=REGISTRATION_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=EMAIL_REGISTRATION_BAD_INPUT_RESPONSE
    ),
    409: openapi.Response(
        description="Existing User", examples=EMAIL_REGISTRATION_EXISITING_USER_RESPONSE
    ),
}

PHONE_REGISTRATION_RESPONSES = {
    201: openapi.Response(
        description="Created User", examples=REGISTRATION_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=PHONE_REGISTRATION_BAD_INPUT_RESPONSE
    ),
    409: openapi.Response(
        description="Existing User", examples=PHONE_REGISTRATION_EXISITING_USER_RESPONSE
    ),
}

COMPLETE_REGISTRATION_RESPONSES = {
    200: openapi.Response(
        description="Complete User Signup",
        examples=COMPLETE_REGISTRATION_SUCCESS_RESPONSE,
    ),
    400: openapi.Response(
        description="Bad Input", examples=COMPLETE_REGISTRATION_BAD_INPUT_RESPONSE
    ),
}


LOGIN_WITH_EMAIL_RESPONSES = {
    200: openapi.Response(
        description="Successful Login", examples=LOGIN_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=LOGIN_WITH_EMAIL_BAD_INPUT_RESPONSE
    ),
    401: openapi.Response(
        description="Invalid Credentials",
        examples=LOGIN_WITH_EMAIL_UNAUTHORISED_RESPONSE,
    ),
}

LOGIN_WITH_PHONE_RESPONSES = {
    200: openapi.Response(
        description="Successful Login", examples=LOGIN_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=LOGIN_WITH_PHONE_BAD_INPUT_RESPONSE
    ),
    401: openapi.Response(
        description="Invalid Credentials",
        examples=LOGIN_WITH_PHONE_UNAUTHORISED_RESPONSE,
    ),
}

PASSWORD_RESET_INITIATE_RESPONSES = {
    200: openapi.Response(
        description="Password Reset Initiate Success",
        examples=PASSWORD_RESET_INITIATE_SUCCESS_RESPONSE,
    ),
    400: openapi.Response(
        description="Bad Input", examples=PASSWORD_RESET_INITIATE_BAD_INPUT_RESPONSE
    ),
}

PASSWORD_RESET_VALIDATE_RESPONSES = {
    200: openapi.Response(
        description="Password Reset Validate Success",
        examples=PASSWORD_RESET_VALIDATE_SUCCESS_RESPONSE,
    ),
    400: openapi.Response(
        description="Bad Input", examples=PASSWORD_RESET_VALIDATE_BAD_INPUT_RESPONSE
    ),
}

SET_AVATAR_SUCCESS_RESPONSE = {"application/json": {"data": True}}

SET_AVATAR_BAD_INPUT_RESPONSE = {
    "application/json": {"errors": {"image": ["This field is required."]}}
}

SET_AVATAR_RESPONSES = {
    200: openapi.Response(
        description="Set Avatar Success", examples=SET_AVATAR_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=SET_AVATAR_BAD_INPUT_RESPONSE
    ),
}

PASSWORD_RESET_FINALIZE_RESPONSES = {
    200: openapi.Response(
        description="Password Reset Finalize Success",
        examples=PASSWORD_RESET_FINALIZE_SUCCESS_RESPONSE,
    ),
    400: openapi.Response(
        description="Bad Input", examples=PASSWORD_RESET_FINALIZE_BAD_INPUT_RESPONSE
    ),
}

EMAIL_VERIFICATION_SUCCESS_RESPONSE = {
    "application/json": {"data": {"completed": True, "action": "EMAIL_VERIFICATION"}}
}

EMAIL_VERIFICATION_OUTPUT_RESPONSES = {
    200: openapi.Response(
        description="Verification Resend Success",
        examples=EMAIL_VERIFICATION_SUCCESS_RESPONSE,
    )
}

PHONE_VERIFICATION_SUCCESS_RESPONSE = {
    "application/json": {"data": {"completed": True, "action": "PHONE_VERIFICATION"}}
}


PHONE_VERIFICATION_OUTPUT_RESPONSES = {
    200: openapi.Response(
        description="Verification Resend Success",
        examples=PHONE_VERIFICATION_SUCCESS_RESPONSE,
    )
}

LOGOUT_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "successfully logged out"}
}

LOGOUT_RESPONSES = {
    200: openapi.Response(
        description="Successfully logged out", examples=LOGIN_SUCCESS_RESPONSE
    )
}

CHANGE_PASSWORD_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "password changed successfully"}
}

CHANGE_PASSWORD_BAD_INPUT_RESPONSE = {
    "application/json": [
        {"errors": {"old_password": ["Password is incorrect"]}},
        {"message": "Old password cannot be same as new password"},
    ]
}


GET_USER_DATA_ERROR = {"application/json": [{"message": "Token is invalid or expired"}]}

USER_DATA_EXAMPLE = {
    "id": "07adf107f41c48d282dea1438bdf41a3",
    "first_name": "Danny",
    "last_name": "reigns",
    "street_address": None,
    "city": None,
    "state_of_residence": None,
    "bio": "",
    "education_level": None,
    "email_verified": True,
    "phone_verified": False,
    "state": "ACTIVE",
    "user_types": ["STAFF", "CONSUMER"],
    "email": "dannyreigns015@gmail.com",
    "phone_number": "07037265628",
    "last_login": "2021-12-03T13:27:03.880722Z",
    "provider": {
        "company_name": "Osnuf Comp And Co.",
        "type": {"name": "ASI", "identifier": "AI"},
        "status": "APPROVED",
        "member": False,
    },
    "created_at": "2021-11-16T16:02:34.635435Z",
    "updated_at": "2021-12-03T13:27:03.891243Z",
    "avatar_url": None,
    "role": None,
    "created_by": None,
    "updated_by": None,
    "deleted_by": None,
    "next_stage": None,
    "last_completed_stage": "COMPLETED_SIGN_UP",
}


USER_EXAMPLE = {
    "first_name": "Funso",
    "last_name": "Joba",
    "email": "hrfunsojoba@gmail.com",
    "phone_number": "08099088978",
    "city": "Ajah",
    "state": "Lagos",
    "country": "Nigeria",
    "user_type": "USER",
    "avatar": None,
}
USER_DATA = {"application/json": {"data": USER_EXAMPLE, "message": ""}}


CHANGE_PASSWORD_RESPONSES = {
    200: openapi.Response(
        description="Password Changed Successfully",
        examples=CHANGE_PASSWORD_SUCCESS_RESPONSE,
    ),
    400: openapi.Response(
        description="Wrong Password Input", examples=CHANGE_PASSWORD_BAD_INPUT_RESPONSE
    ),
}


GET_USER_DATA = {
    200: openapi.Response(
        description="retrieved user data successfully", examples=USER_DATA
    ),
    403: openapi.Response(description="Unathorized", examples=GET_USER_DATA_ERROR),
}
