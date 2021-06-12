# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Parking_Slot_App.py'],
             pathex=['C:\\Users\\LENOVO\\ParkingSlot\\Slot\\GUI\\GUI App\\FIX'],
             binaries=[],
             datas=[('gifz.gif','.'),('assets/yolov4-obj_best.weights','assets'),('assets/yolov4-obj.cfg','assets'),('assets/obj.names','assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Parking_Slot_App',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Parking_Slot_App')
