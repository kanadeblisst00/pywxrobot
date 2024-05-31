# https://github.com/zhangxiaoyang/WechatImageDecoder
# zhangxiaoyang.hit[at]gmail.com

import re


class WechatImageDecoder:
    def __init__(self):
        pass

    def decode_pc_dat(self, dat_file, save_path):
        
        def do_magic(header_code, buf):
            return header_code ^ list(buf)[0] if buf else 0x00
        
        def decode(magic, buf):
            return bytearray([b ^ magic for b in list(buf)])
            
        def guess_encoding(buf):
            headers = {
                'jpg': (0xff, 0xd8),
                'png': (0x89, 0x50),
                'gif': (0x47, 0x49),
            }
            for encoding in headers:
                header_code, check_code = headers[encoding] 
                magic = do_magic(header_code, buf)
                _, code = decode(magic, buf[:2])
                if check_code == code:
                    return (encoding, magic)
            raise Exception(f"图片未知格式, 图片路径: {dat_file}!")

        with open(dat_file, 'rb') as f:
            buf = bytearray(f.read())
        file_type, magic = guess_encoding(buf)
        path = save_path.rsplit(".", 1)[0] 
        with open(f"{path}.{file_type}", 'wb') as f:
            new_buf = decode(magic, buf)
            f.write(new_buf)

    def decode_android_dat(self, dat_file):
        with open(dat_file, 'rb') as f:
            buf = f.read()

        last_index = 0
        for i, m in enumerate(re.finditer(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46', buf)):
            if m.start() == 0:
                continue

            imgfile = '%s_%d.jpg' % (dat_file, i)
            with open(imgfile, 'wb') as f:
                f.write(buf[last_index: m.start()])
            last_index = m.start()


if __name__ == '__main__':
    pass
