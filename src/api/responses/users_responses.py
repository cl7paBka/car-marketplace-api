# Responses for end-points in src/api/users.py

# users/create

create_user_responses = {
    409: {
        "description": "User with the given email already exists",
        "content": {
            "application/json": {
                "examples": {
                    "duplicate_email": {
                        "summary": "Duplicate email",
                        "value": {
                            "detail": "User with email: 'user@example.com' already exists."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "database_error": {
                        "summary": "Database error",
                        "value": {
                            "detail": "Internal database error: <error details>"
                        }
                    }
                }
            }
        }
    },
}

# users/{user_id}
get_user_by_id_responses = {
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "User does not exist",
                        "value": {
                            "detail": "User with id: '1' does not exist."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}

# users/email/{user_email}
get_user_by_email_responses = {
    404: {
        "description": "User not found by email",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Email not found",
                        "value": {
                            "detail": "User with email: 'user@example.com' does not exist."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}

# users/role/{role}
get_users_by_role_responses = {
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}

# users/
get_all_users_responses = {
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}

# users/patch/{user_id}
update_user_responses = {
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "User does not exist",
                        "value": {
                            "detail": "User with id: '1' does not exist."
                        }
                    }
                }
            }
        }
    },
    409: {
        "description": "Conflict: Email already exists",
        "content": {
            "application/json": {
                "examples": {
                    "duplicate_email": {
                        "summary": "Duplicate email",
                        "value": {
                            "detail": "User with email: 'updated_user@example.com' already exists."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}

# users/delete/{user_id}
delete_user_responses = {
    200: {
        "description": "User successfully deleted",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "User deleted",
                        "value": {
                            "status": "success",
                            "message": "User with id 1 deleted."
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "User does not exist",
                        "value": {
                            "detail": "User with id: '1' does not exist."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}
