#!/bin/bash

# initwelcome.sh: sets welcome screen
# Execute once only

# Greeting Text
curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"greeting",
  "greeting":{
    "text":"Hi {{user_first_name}}, welcome to QuickRead! Please enter a URL for us to summarize for you."
  }
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAAH2jdKoLmwBAMyURBrrfPjBf6564qclWZB9RbWD0e513q9B3Rd0kWU9X0DeZBMgAYojBWRE0pcmZBMlE9JULumFV5hpqxoYwhq68JkpimZCDi5vrc0QksztdI2pZBfqY1ZBtZBjBvG0p74xnhwXLjS6jQXMZBnjxcTCA1ZBuBPyC9QZDZD"

# Get Started button
curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"call_to_actions",
  "thread_state":"new_thread",
  "call_to_actions":[
    {
      "payload":"Get Started"
    }
  ]
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAAH2jdKoLmwBAMyURBrrfPjBf6564qclWZB9RbWD0e513q9B3Rd0kWU9X0DeZBMgAYojBWRE0pcmZBMlE9JULumFV5hpqxoYwhq68JkpimZCDi5vrc0QksztdI2pZBfqY1ZBtZBjBvG0p74xnhwXLjS6jQXMZBnjxcTCA1ZBuBPyC9QZDZD"