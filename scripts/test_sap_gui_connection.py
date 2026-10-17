import win32com.client

sap_gui = win32com.client.GetObject("SAPGUI")
application = sap_gui.GetScriptingEngine

print("Connections:", application.Children.Count)

connection = application.Children(0)
print("Sessions:", connection.Children.Count)

session = connection.Children(0)

print("System:", session.Info.SystemName)
print("Client:", session.Info.Client)
print("User:", session.Info.User)
print("Transaction:", session.Info.Transaction)