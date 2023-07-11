#cvzone find hand_box 2 xml
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
from xml.dom.minidom import *

def generate_xml_pre(img, img_name, save_ann_path, box, class_name):
    #图片输入路径,原有的基础上添加的脚本
 
    name1 = img_name.split('.', 3)[0]
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

    for i,bbox in enumerate(box):
        #创建三级节点，循环添加
        annotation6="annotation6"+str(i)
        print(annotation6)
        annotation6=doc.createElement('object')
        name=doc.createElement('name')
        name.appendChild(doc.createTextNode(class_name)) #添加类别名
        #创建一个带着文本节点的子节点
        ceo1=doc.createElement('pose')
        ceo1.appendChild(doc.createTextNode("Unspecified"))
        ceo2=doc.createElement('truncated')
        ceo2.appendChild(doc.createTextNode('0'))
        ceo3=doc.createElement('difficult')
        ceo3.appendChild(doc.createTextNode('0'))

        ceo4 = doc.createElement('bndbox')

        #print bbox[0], type(bbox[0]),
        xmin = bbox[0]
        ymin =  bbox[1] 
        xmax =  bbox[2] 
        ymax =  bbox[3] 

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

        root.appendChild(annotation6)




    #将节点信息添加到roo下
    root.appendChild(annotation1)
    root.appendChild(annotation2)
    root.appendChild(annotation3)
    root.appendChild(annotation4)
    root.appendChild(annotation)
    root.appendChild(annotation5)
    #root.appendChild(annotation6)

    #print(doc.toxml())
    #存成xml文件的位置
    print(save_ann_path,name1)
    filename1= save_ann_path +name1+'.xml'
 
    fp = open(filename1, 'w')
    doc.writexml(fp, indent='', addindent='\t', newl='\n')
    fp.close()
if __name__ == "__main__":

    pic_path='E:/datasets/3.1hand_gesture/v5-9/slected_TFS/selected1/three/'
    save_path='E:/datasets/3.1hand_gesture/v5-9/slected_TFS/selected2/stop/ann_img/'
    an_path='E:/datasets/3.1hand_gesture/v5-9/slected_TFS/selected1/ann_three/'
    class_name = "three"  #
    detector = HandDetector(mode=True,detectionCon=0.8, maxHands=2)
    filelist=os.listdir(pic_path)
    
    for item in filelist:
        boxlist=[]
        img=cv2.imread(pic_path+item)
        # Find the hand and its landmarks
        hands=[] 
        hands = detector.findHands(img,draw=False)   
        #hands,img = detector.findHands(img,draw=False)            
        print(len(hands))
        for i in hands:
            bbox = i["bbox"]  # Bounding box info x,y,w,h 
            x1= bbox[0] - 20
            y1= bbox[1] - 20
            x2= bbox[0] + bbox[2] + 20
            y2= bbox[1] + bbox[3] + 20
            cv2.rectangle(img, (int(x1), int(y1)),(int(x2), int(y2)),(0, 0, 255), 1)
            
            print("x1,y1,x2,y2",x1,y1,x2,y2)
            
            boxlist.append([x1,y1,x2,y2])
        generate_xml_pre(img, item, an_path,boxlist, class_name)
        cv2.imwrite(save_path+item,img)
    
