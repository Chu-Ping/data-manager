import json
import json_io

def squeeze(text:str) -> str:
    if text[-1] == " ":
        text = squeeze(text[:-1])
    return text
    
class Database:
    fname = '.datadescription'
    fname_base = '.database'
    metadata = {
        'path': '',
        'from': '',
        'date': '',
        'associate': '',
        'description': ''
    }

    @staticmethod     
    def _search(data: list, key: str, value) -> list: 
        ret = []
        for d in data:
            if value in d[key]: ret.append(d)
        return ret

    def search(self, addr, search_list):
        '''
        search_list: list of (key, value)
        '''
        addr = squeeze(addr)
        data = json_io.read_json(addr + '/' + self.fname_base)
        for key, value in search_list:
            data = self._search(data, key, value)
        return data

    def create_base(self, root_addr): 
        root_addr = squeeze(root_addr)
        files = []
        files = json_io.recursive_search(root_addr, self.fname, files)
        json_data = []
        for file in files:
            json_data.append(json_io.read_json(file))

        with open(root_addr + '/' + self.fname_base,'w+') as f:
            json.dump(json_data, f, indent=4)

    def create(self, values, addr):
        addr = squeeze(addr)
        for ((key, _), value) in zip(self.metadata.items(), values):
            self.metadata[key] = value
        
        with open(addr + '/' + self.fname,'w+') as f:
            json.dump(self.metadata, f, indent=4)

if __name__ == "__main__":
    db = Database()

    db.create_base(r'C:\Users\chu-ping.yu\OneDrive - Thermo Fisher Scientific\data')

