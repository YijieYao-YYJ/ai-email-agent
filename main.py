# from agent import run_agent
#
#
# email = """
# Hallo,
#
# ich bin Kunde C001.
# Meine Bestellung 12345 ist noch nicht angekommen.
#
# Können Sie bitte meine Kundendaten und
# den Bestellstatus prüfen?
#
# Viele Grüße
# Max
# """
#
# answer = run_agent(email)
#
# print("\n--- Final Answer ---")
# print(answer)


from agent import run_agent


email = """
Hallo,

meine E-Mail-Adresse ist max@example.com.
Wo ist meine Bestellung?

Viele Grüße
"""

answer = run_agent(email)

print("\n--- Final Answer ---")
print(answer)