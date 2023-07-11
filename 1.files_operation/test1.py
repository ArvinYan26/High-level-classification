def generate_xml_pre(img, img_name, save_ann_path, box):
    #图片输入路径,原有的基础上添加的脚本
    #IMAGE_DIR = os.path.join(ROOT_DIR, img_path)
    
    #IMAGE_files=os.listdir(IMAGE_DIR)
    #for annotation_filename in IMAGE_files:
    name1 = img_name.split('.', 3)[0]
    #mat_img = cv.imread(img + annotation_filename)
    [height, width, c] = img.shape
    doc = Document()      #xml base
    root=doc.createElement('annotation')
    doc.appendChild(root)

    annotation1=doc.createElement('folder')
    annotation1.appendChild(doc.createTextNode('test_none'))

    annotation2=doc.createElement('filename')
    annotation2.appendChild(doc.createTextNode(img_name))

    annotation3=doc.createElement('path')
    name9 = img_name   #img path,you can give the path by yourself
    annotation3.appendChild(doc.createTextNode(name9))

    annotation4=doc.createElement('source')
    name5=doc.createElement('database')
    name5.appendChild(doc.createTextNode('Unknown'))
    annotation4.appendChild(name5)

    # 创建二级节点
    annotation = doc.createElement('size')
    name = doc.createElement('width')
    name.appendChild(doc.createTextNode(str(width)))  # 添加文本节点
    # 创建一个带着文本节点的子节点
    ceo1 = doc.createElement('height')
    ceo1.appendChild(doc.createTextNode(str(height)))
    ceo = doc.createElement('depth')
    ceo.appendChild(doc.createTextNode('3'))
    annotation.appendChild(name)  # name加入到company
    annotation.appendChild(ceo1)
    annotation.appendChild(ceo)

    annotation5=doc.createElement('segmented')
    annotation5.appendChild(doc.createTextNode('0'))

    #创建三级节点，循环添加
    annotation6=doc.createElement('object')
    name=doc.createElement('name')
    name.appendChild(doc.createTextNode("hand")) #添加类别名
    #创建一个带着文本节点的子节点
    ceo1=doc.createElement('pose')
    ceo1.appendChild(doc.createTextNode("Unspecified"))
    ceo2=doc.createElement('truncated')
    ceo2.appendChild(doc.createTextNode('0'))
    ceo3=doc.createElement('difficult')
    ceo3.appendChild(doc.createTextNode('0'))

    ceo4 = doc.createElement('bandbox')
    for bbox in box:
        #print bbox[0], type(bbox[0]),
        xmin = int(round(bbox[0]) - round(bbox[2] / 2))
        ymin = int(round(bbox[1]) - round(bbox[3] / 2))
        xmax = int(round(bbox[0]) + round(bbox[2] / 2))
        ymax = int(round(bbox[1]) + round(bbox[3] / 2))

        c1 = ceo4.appendChild(doc.createElement("xmin"))
        c1.appendChild(doc.createTextNode(str(xmin)))
        c2 = ceo4.appendChild(doc.createElement("ymin"))
        c2.appendChild(doc.createTextNode(str(ymin)))
        c3 = ceo4.appendChild(doc.createElement("xmax"))
        c3.appendChild(doc.createTextNode(str(xmax)))
        c4 = ceo4.appendChild(doc.createElement("ymax"))
        c4.appendChild(doc.createTextNode(str(ymax)))
        ceo4.appendChild(c1)
        ceo4.appendChild(c2)
        ceo4.appendChild(c3)
        ceo4.appendChild(c4)

        annotation6.appendChild(name) #name加入到company
        annotation6.appendChild(ceo1)
        annotation6.appendChild(ceo2)
        annotation6.appendChild(ceo3)
        annotation6.appendChild(ceo4)

    #将节点信息添加到roo下

    root.appendChild(annotation1)
    root.appendChild(annotation2)
    root.appendChild(annotation3)
    root.appendChild(annotation4)
    root.appendChild(annotation)
    root.appendChild(annotation5)
    root.appendChild(annotation6)

    print(ceo.tagName)
    print(doc.toxml())
    #存成xml文件的位置
    filename1= save_ann_path + name1+'.xml'
    #print filename1
    #fp = open(filename1, 'w', encoding='utf-8')
    fp = open(filename1, 'w')
    doc.writexml(fp, indent='', addindent='\t', newl='\n')
    fp.close()
