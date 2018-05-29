# -*- mode: python -*-

block_cipher = None


a = Analysis(['accounts_code_generation.py'],
             pathex=['C:\\Users\\shil4046\\Dev\\Accounts-Code-Generation'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='accounts_code_generation',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
