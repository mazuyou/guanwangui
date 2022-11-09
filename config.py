from ruamel import yaml
import os
import configparser


#写入yaml
def yamlWrite(xml_path,configname):
    curpath = os.path.dirname(os.path.realpath(__file__))
    yamlpath = os.path.join(curpath,configname)
    with open(yamlpath, "a", encoding="utf8") as f:
        yaml.dump(xml_path, f, Dumper=yaml.RoundTripDumper,allow_unicode=True)

#读取yaml文件
def yamlRead(configpath):
    f = open(configpath,"r",encoding="utf8")
    data = f.read()
    yaml_reader = yaml.load(data,Loader=yaml.Loader)
    return yaml_reader

#写入ini
def iniWrite(path,url,key,value):
    cfg = configparser.ConfigParser()
    cfg.add_section(url)
    cfg.set(url,key,value)
    cfg.write(open(path,"a",encoding="utf8"))
    print("写入成功")

#读取ini
def iniRead(path):
    cfg = configparser.ConfigParser()
    cfg.read(path,encoding="utf8")
    return cfg

# a = {"中文":"sda","中国":"sdadasd"}
# b = "www.baidu.com"
# c = {}
# c[b] = a
# yamlWrite(c,"config.yaml")
# print(yamlRead("config.yaml"))
if __name__ == '__main__':
    print(yamlRead("config.yaml"))