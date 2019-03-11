from ScoutSuite.providers.base.configs.resources import Resources


class SecurityContacts(Resources):

    def __init__(self, facade):
        self.facade = facade

    async def fetch_all(self):
        for raw_contact in await self.facade.get_security_contacts():
            id, security_contact = self._parse(raw_contact)
            self[id] = security_contact

    def _parse(self, security_contact):
        security_contact_dict = {}
        security_contact_dict['id'] = security_contact.id
        security_contact_dict['name'] = security_contact.name
        security_contact_dict['email'] = security_contact.email
        security_contact_dict['phone'] = security_contact.phone
        security_contact_dict['alert_notifications'] = security_contact.alert_notifications == "On"
        security_contact_dict['alerts_to_admins'] = security_contact.alerts_to_admins == "On"
        security_contact_dict['additional_properties'] = security_contact.additional_properties

        return security_contact_dict['id'], security_contact_dict
