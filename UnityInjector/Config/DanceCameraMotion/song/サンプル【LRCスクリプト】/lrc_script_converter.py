import sys, os, re, copy
import logging, argparse
import xml.etree.ElementTree as ElementTree

script_name = 'LRC Script to DCM Converter ver1.0.0'

logger = logging.getLogger(__name__)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)

class LrcScriptConverter:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path
        self.src_file = os.path.basename(self.src_path)

        self.metronome = 120.0
        self.base_note = 4.0
        self.end_time = 60.0
        self.offset = 0.0

        self.errors = []

    def error(self, message):
        logger.error('[ERROR]' + message)
        self.errors.append(message)

    def hasErrors(self):
        return len(self.errors) > 0

    def dumpErrors(self):
        for message in self.errors:
            logger.error('[ERROR]' + message)

    def nextTime(self, lines, i):
        time = lines[i][0]
        for j in range(len(lines) - i):
            t = lines[i + j][0]
            if t > time:
                return t

        return self.end_time

    def writeCsv(self, prefix, header, lines):
        path = os.path.join(self.dst_path, prefix + os.path.splitext(self.src_file)[0] + '.csv')
        logger.info('csv出力: ' + path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(header + "\n")
            for i in range(len(lines)):
                time = lines[i][0]
                line = lines[i][1]

                if line is not None and len(line) > 0:
                    next_time = self.nextTime(lines, i)
                    next_frame = int(next_time * 30)

                    # 出力時変数の置換
                    m_iter = re.finditer(r'(\$[a-z0-9_]+)', line)
                    for m in m_iter:
                        g = m.groups()
                        if len(g) == 1:
                            logger.debug('出力時変数の置換: ' + str(g))
                            name = g[0]
                            if name == '$csv_next':
                                line = line.replace('$csv_next', str(next_time))
                            elif name == '$csv_next_frame':
                                line = line.replace('$csv_next_frame', str(next_frame))
                            else:
                                self.error('未定義の変数 name:' + name + ' line:' + line)

                    # 演算処理
                    m_iter = re.finditer(r'\$\(([^)]+)\)', line)
                    for m in m_iter:
                        g = m.groups()
                        if len(g) == 1:
                            logger.debug('演算処理: ' + str(g))
                            formula = g[0]
                            result = eval(formula, {})
                            line = line.replace('$(' + formula + ')', str(result))

                    f.write(line + "\n")

    def run(self):
        if self.src_file == 'template.lrc':
            self.error('template.lrcというファイル名は使えません')
            return

        logger.info('変換中: ' + self.src_path)

        # movePngのテンプレ読み込み
        move_png_template = None
        move_png_template_groups = {}
        move_png_template_path = os.path.join(self.dst_path, 'movePng_template.xml')

        if os.path.isfile(move_png_template_path):
            move_png_template = ElementTree.parse(move_png_template_path)
            for png_group in move_png_template.getroot():
                label = png_group.attrib['label']
                move_png_template_groups[label] = png_group

        # movePng初期化
        move_png = None
        move_png_groups = {}
        move_png_path = os.path.join(self.dst_path, 'movePng_' + os.path.splitext(self.src_file)[0] + '.xml')

        # movePngをテンプレから生成
        if move_png_template is not None:
            move_png = copy.deepcopy(move_png_template)

            for png_group in move_png.getroot():
                label = png_group.attrib['label']
                move_png_groups[label] = png_group
                remove_childlen = []
                for child in png_group:
                    if child.tag == 'png':
                        remove_childlen.append(child)
                for child in remove_childlen:
                    png_group.remove(child)

        # ラインの読み取り
        lines = []
        with open(self.src_path, 'r', encoding='utf-8') as f:
            for l in f.readlines():
                m = re.match(r'\[([0-9]+):([0-9]+)\.([0-9]+)\](.+)', l)
                g = m.groups() if m is not None else []

                if len(g) == 4:
                    logger.debug('ラインの読み取り: ' + str(g))
                    line = g[3]

                    # コメント削除
                    line = re.sub(r'##.*', '', line)

                    sec = int(g[0]) * 60 + int(g[1])
                    time = float(str(sec) + '.' + g[2])
                    lines.append((time, line.strip()))

        # タグ情報格納用
        lyrics = []
        faces = []
        morphs = []
        posef = []
        posem = []
        texts = []
        mabataki = []
        cameras = []
        bgs = []
        lights = []
        fade = []
        menu = []
        undress = []
        shape = []
        eyes = []
        custom_tags = {}

        # ラインの処理
        for i in range(len(lines)):
            logger.debug('ラインの処理: ' + str(lines[i]))
            time = max(lines[i][0] + self.offset, 0.0)
            line = lines[i][1]

            frame = int(time * 30)
            next_time = max(self.nextTime(lines, i) + self.offset, 0.0)
            next_frame = int(next_time * 30)

            # カスタムタグの定義
            custom_tag_found = False
            m_iter = re.finditer(r'(#[A-Z0-9_]+) *(\+?)=(.+)', line)
            for m in m_iter:
                g = m.groups()
                if len(g) == 3:
                    logger.debug('カスタムタグの定義: ' + str(g))
                    tag = g[0]
                    ope = g[1]
                    data = g[2]
                    if ope == '+':
                        custom_tags[tag] += data
                    else:
                        custom_tags[tag] = data
                    custom_tag_found = True

            if custom_tag_found:
                continue

            # カスタムタグの置換
            m_iter = re.finditer(r'(#[A-Z0-9_]+)(:[^#]+)?', line)
            for m in m_iter:
                g = m.groups()
                if len(g) == 2:
                    tag = g[0]
                    if tag in custom_tags:
                        logger.debug('カスタムタグの置換: ' + str(g))
                        data = custom_tags[tag]
                        if g[1] is not None:
                            args = g[1].strip(':').strip().split(',')
                            for j in range(len(args)):
                                data = data.replace('$' + str(j + 1), args[j])
                        if re.search(r'\$[0-9]+', data) is not None:
                            self.error('引数が足りません tag:' + tag + ' line:' + line)
                            data = ''
                        line = re.sub(tag + '(:[^#]+)?', data, line)

            # 変数の置換
            m_iter = re.finditer(r'(\$[a-z0-9_]+)', line)
            for m in m_iter:
                g = m.groups()
                if len(g) == 1:
                    logger.debug('変数の置換: ' + str(g))
                    name = g[0]
                    if name == '$now':
                        line = line.replace('$now', str(time))
                    elif name == '$next':
                        line = line.replace('$next', str(next_time))
                    elif name == '$end':
                        line = line.replace('$end', str(self.end_time))
                    elif name == '$frame':
                        line = line.replace('$frame', str(frame))
                    elif name == '$next_frame':
                        line = line.replace('$next_frame', str(next_frame))

            # タグの処理
            m_iter = re.finditer(r'(#[A-Z0-9_]+)(:[^#]+)?', line)
            for m in m_iter:
                g = m.groups()
                if len(g) == 2:
                    logger.debug('タグの処理: ' + str(g))
                    tag = g[0]
                    data = g[1].strip(':').strip() if g[1] is not None else None
                    if tag == '#METRONOME':
                        self.metronome = float(data)
                    elif tag == '#BASE_NOTE':
                        self.base_note = float(data)
                    elif tag == '#END_TIME':
                        self.end_time = float(data)
                    elif tag == '#OFFSET':
                        self.offset = float(data)
                    elif tag == '#FACE':
                        faces.append((time, data))
                    elif tag == '#MORPH':
                        morphs.append((time, data))
                    elif tag == '#POSE_F':
                        posef.append((time, data))
                    elif tag == '#POSE_M':
                        posem.append((time, data))
                    elif tag == '#TEXT':
                        texts.append((time, data))
                    elif tag == '#MABATAKI':
                        mabataki.append((time, data))
                    elif tag == '#CAMERA':
                        cameras.append((time, data))
                    elif tag == '#BG':
                        bgs.append((time, data))
                    elif tag == '#LIGHT':
                        lights.append((time, data))
                    elif tag == '#FADE':
                        fade.append((time, data))
                    elif tag == '#MENU':
                        menu.append((time, data))
                    elif tag == '#UNDRESS':
                        undress.append((time, data))
                    elif tag == '#SHAPE':
                        shape.append((time, data))
                    elif tag == '#EYES':
                        eyes.append((time, data))
                    elif tag == '#MOVE_PNG':
                        args = data.split(',')
                        label = args[0]
                        generate_type = args[1]
                        loop_interval = float(args[2])
                        if label in move_png_groups:
                            move_png_group = move_png_groups[label]
                            move_png_template_group = move_png_template_groups[label]
                            if generate_type == 'expand':
                                for child in move_png_template_group:
                                    if child.tag == 'png':
                                        new_child = copy.deepcopy(child)
                                        new_child.attrib['startTime'] = str(time)
                                        new_child.attrib['endTime'] = str(next_time)
                                        move_png_group.append(new_child)
                            elif generate_type == 'repeat':
                                t = time
                                while t < next_time:
                                    for child in move_png_template_group:
                                        if child.tag == 'png':
                                            start_t = float(child.attrib['startTime']) + t
                                            end_t = float(child.attrib['endTime']) + t
                                            if start_t < next_time:
                                                new_child = copy.deepcopy(child)
                                                new_child.attrib['startTime'] = str(start_t)
                                                new_child.attrib['endTime'] = str(end_t)
                                                move_png_group.append(new_child)
                                    if loop_interval <= 0.0: break
                                    t += loop_interval
                            else:
                                self.error('未定義の生成タイプ generate_type:' + generate_type)
                    else:
                        self.error('未定義のタグ tag:' + tag + ' line:' + line)

            # タグを削除
            line = re.sub(r'#.+', '', line).strip()

            # 括弧削除
            line = re.sub(r'(?<!\$)\([^)]+\)', '', line).strip()

            # 口パク用処理
            if len(line) > 0:

                # 繰り返し文字の適用
                m = re.match(r'\{(.+)\}', line)
                if m and len(m.groups()) > 0:
                    loop_str = m.groups()[0]
                    diff = next_time - time
                    char_time = (60.0 / self.metronome) / (self.base_note / 4.0)
                    char_count = int(diff / char_time)
                    loop_str = loop_str * (int(char_count / len(loop_str)) + 1)
                    line = re.sub(r'\{.+\}', loop_str[:char_count], line)

                data = str(time) + ',' + line
                lyrics.append((time, data))

        # 口パクの出力
        self.writeCsv(
            prefix='lyrics_',
            header="time,lyrics",
            lines=lyrics,
        )

        # ダンス表情の出力
        self.writeCsv(
            prefix='face_',
            header="time,face,blend",
            lines=faces,
        )

        # ポーズFの出力
        self.writeCsv(
            prefix='pose_f_',
            header="time,poseType,animation,fadeTime,speed,posX,posY,posZ,rotX,rotY,rotZ,eyeMoveType,option",
            lines=posef,
        )

        # ポーズMの出力
        self.writeCsv(
            prefix='pose_m_',
            header="time,poseType,animation,fadeTime,speed,posX,posY,posZ,rotX,rotY,rotZ,eyeMoveType,option,targetMaidSlotNo,posHeadBaseX,posHeadBaseY,posHeadBaseZ",
            lines=posem,
        )

        # テキストの出力
        self.writeCsv(
            prefix='text_',
            header="index,text,font,fontSize,stTime,stPosX,stPosY,stRotZ,stScaX,stScaY,stColR,stColG,stColB,stColA,edTime,edPosX,edPosY,edRotZ,edScaX,edScaY,edColR,edColG,edColB,edColA,easing,lineSpacing,alignment,sizeDeltaX,sizeDeltaY",
            lines=texts,
        )

        # 背景の出力
        self.writeCsv(
            prefix='bg_',
            header="bgName,group,time,posX,posY,posZ,rotX,rotY,rotZ,scale",
            lines=bgs,
        )

        # 照明の出力
        self.writeCsv(
            prefix='light_',
            header="type,group,stTime,stPosX,stPosY,stPosZ,stRotX,stRotY,stRotZ,stColR,stColR,stColB,edTime,edPosX,edPosY,edPosZ,edRotX,edRotY,edRotZ,edColR,edColG,edColB,option,range,intensity,spotAngle,maidSlotNo",
            lines=lights,
        )

        # まばたきの出力
        self.writeCsv(
            prefix='mabataki_',
            header="startFrame,endFrame",
            lines=mabataki,
        )

        # 表情タイムラインの出力
        self.writeCsv(
            prefix='morph_',
            header="frame,morphName,morphValue",
            lines=morphs,
        )

        # カメラタイムラインの出力
        self.writeCsv(
            prefix='camera_',
            header="frame,posX,posY,posZ,rotX,RotY,rotZ,distance,viewAngle,easing",
            lines=cameras,
        )

        # フェードの出力
        self.writeCsv(
            prefix='fade_',
            header="stTime,edTime,inTime,outTime,isWhite",
            lines=fade,
        )

        # メニューの出力
        self.writeCsv(
            prefix='menu_',
            header="tag,menu,slotNo,time",
            lines=menu,
        )

        # 脱衣の出力
        self.writeCsv(
            prefix='undress_',
            header="label,maidSlotNo,time,isMask",
            lines=undress,
        )

        # シェイプキーの出力
        self.writeCsv(
            prefix='shape_',
            header="stTime,edTime,maidSlotNo,tag,slot,minSize,maxSize,outInterval,inInterval,outKeepTime,inKeepTime,outEasing,inEasing,isOneWay,isReverse",
            lines=shape,
        )

        # 瞳の出力
        self.writeCsv(
            prefix='eyes_',
            header="type,startTime,startHorizon,startVertical,endTime,endHorizon,endVertical,easing",
            lines=eyes,
        )

        # movePngの出力
        if move_png is not None:
            logger.info('movePng出力: ' + move_png_path)
            move_png.write(
                move_png_path,
                encoding='utf-8',
                short_empty_elements=False,
                xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=script_name)
    parser.add_argument('--log-level', help='Log Level. (DEBUG|INFO|WARNING)')
    args = parser.parse_args()

    default_log_level = 'DEBUG' if "debugpy" in sys.modules else 'INFO'
    logger.setLevel(args.log_level or default_log_level)

    logger.info('====================================')
    logger.info(script_name)
    logger.info('====================================')

    work_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    files = os.listdir(path=work_path)
    files = [f for f in files if os.path.splitext(f)[1] == '.lrc']

    for file in files:
        converter = LrcScriptConverter(
            src_path=os.path.join(work_path, file),
            dst_path=work_path)

        converter.run()

        if converter.hasErrors():
            logger.info('エラーが発生しました。ログを確認してください')
            converter.dumpErrors()
            exit(1)

    logger.info('すべての処理が完了しました')
