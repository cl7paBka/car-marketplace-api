# Responses for end-points in src/api/orders.py
# post orders/create
create_order_responses = {
    400: {
        "description": "Invalid role or input data",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_role": {
                        "summary": "User does not have the required role",
                        "value": {
                            "detail": "The user with ID: '2' is a manager, not a customer."
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "User, Salesperson, or Car not found",
        "content": {
            "application/json": {
                "examples": {
                    "customer_not_found": {
                        "summary": "Customer not found",
                        "value": {
                            "detail": "Customer with ID: '3' was not found."
                        }
                    },
                    "salesperson_not_found": {
                        "summary": "Salesperson not found",
                        "value": {
                            "detail": "Salesperson with ID: '4' was not found."
                        }
                    },
                    "car_not_found": {
                        "summary": "Car not found",
                        "value": {
                            "detail": "Car with ID: '5' was not found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "database_error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/{order_id}
get_order_by_id_responses = {
    404: {
        "description": "Order not found by ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Order does not exist",
                        "value": {
                            "detail": "Order not found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Database or other error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/status/{status}
get_orders_by_status_responses = {
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "error": {
                        "summary": "Unexpected error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/customer_id/{customer_id}
get_orders_by_customer_id_responses = {
    400: {
        "description": "User with the given ID is not a customer",
        "content": {
            "application/json": {
                "examples": {
                    "wrong_role": {
                        "summary": "Invalid role",
                        "value": {
                            "detail": "The user with ID: '1' is a manager, not a customer."
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Customer not found by the given ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "No such customer",
                        "value": {
                            "detail": "Customer with ID: '1' was not found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "db_error": {
                        "summary": "Error occurred",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/salesperson_id/{salesperson_id}
get_orders_by_salesperson_id_responses = {
    400: {
        "description": "The user with the given ID is not a manager",
        "content": {
            "application/json": {
                "examples": {
                    "wrong_role": {
                        "summary": "Invalid role",
                        "value": {
                            "detail": "The user with ID: '2' is a customer, not a manager."
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Salesperson not found by the given ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "No such salesperson",
                        "value": {
                            "detail": "Salesperson with ID: '2' was not found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "db_error": {
                        "summary": "Error occurred",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/car_id/{car_id}
get_orders_by_car_id_responses = {
    404: {
        "description": "Car not found by the given ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Car does not exist",
                        "value": {
                            "detail": "Car with ID: '10' was not found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "db_error": {
                        "summary": "Error occurred",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/
get_all_orders_responses = {
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "db_error": {
                        "summary": "Error occurred",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# get orders/patch/{order_id}
update_order_responses = {
    400: {
        "description": "Invalid role or other constraints",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_role": {
                        "summary": "Role mismatch",
                        "value": {
                            "detail": "The user with ID: '5' is a manager, not a customer."
                        }
                    },
                    "empty_payload": {
                        "summary": "No fields provided",
                        "value": {
                            "detail": "Payload cannot be empty."
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Order, customer, salesperson, or car not found",
        "content": {
            "application/json": {
                "examples": {
                    "order_not_found": {
                        "summary": "No order by this ID",
                        "value": {
                            "detail": "Order with id: '101' does not exist."
                        }
                    },
                    "customer_not_found": {
                        "summary": "No such customer",
                        "value": {
                            "detail": "Customer with ID: '1' was not found."
                        }
                    },
                    "salesperson_not_found": {
                        "summary": "No such salesperson",
                        "value": {
                            "detail": "Salesperson with ID: '2' was not found."
                        }
                    },
                    "car_not_found": {
                        "summary": "No such car",
                        "value": {
                            "detail": "Car with ID: '10' was not found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Server error",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
# delete orders/delete/{order_id}
delete_order_responses = {
    404: {
        "description": "Order not found by the given ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "No order found",
                        "value": {
                            "detail": "No order with id: '101' found."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "examples": {
                    "db_error": {
                        "summary": "Error occurred",
                        "value": {
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    }
}
