# Responses for end-points in src/api/cars.py
# post cars/add
add_car_responses = {
    409: {
        "description": "Car with the given VIN number already exists",
        "content": {
            "application/json": {
                "examples": {
                    "duplicate_vin": {
                        "summary": "Duplicate VIN",
                        "value": {
                            "detail": "Car with vin_number: 'VIN123456789' already exists."
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
                            "detail": "An unexpected error occurred: <error details>"
                        }
                    }
                }
            }
        }
    },
}
# get cars/{car_id}
get_car_by_id_responses = {
    404: {
        "description": "Car not found by ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Car does not exist",
                        "value": {
                            "detail": "Car not found."
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
# get cars/vin/{vin_number}
get_car_by_vin_responses = {
    404: {
        "description": "Car not found by VIN",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Car does not exist by VIN",
                        "value": {
                            "detail": "Car not found."
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
# get cars/engine/{engine_type}
get_cars_by_engine_responses = {
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
    }
}
# get cars/transmission/{transmission_type}
get_cars_by_transmission_responses = {
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
    }
}
# get cars/
get_all_cars_responses = {
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
    }
}
# patch cars/patch/{car_id}
update_car_responses = {
    404: {
        "description": "Car not found",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Car does not exist",
                        "value": {
                            "detail": "Car with id: '1' does not exist."
                        }
                    }
                }
            }
        }
    },
    409: {
        "description": "Conflict: VIN already exists",
        "content": {
            "application/json": {
                "examples": {
                    "duplicate_vin": {
                        "summary": "Duplicate VIN",
                        "value": {
                            "detail": "Car with vin_number: 'VIN123456789' already exists."
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
# delete cars/delete/{car_id}
delete_car_responses = {
    404: {
        "description": "Car not found by ID",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Car does not exist",
                        "value": {
                            "detail": "No car with id: '1' found."
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
