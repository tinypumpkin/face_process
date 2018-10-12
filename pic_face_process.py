#coding: utf-8


import cv2
import dlib
import numpy as np



class face_emotion():
    """
    对一个文件夹中的所有照片的所有人脸进行识别
    然后由面部68特征点进行表情分析
    """
    def __init__(self):
        #self.image=image
        # 使用特征提取器get_frontal_face_detector
        self.detector = dlib.get_frontal_face_detector()
        # dlib的68点模型，使用作者训练好的特征预测器
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


    def fit_slr(self, x, y):
        """简单线性拟合，计算拟合直线的斜率，用来分析眉毛的倾斜程度"""
        n = len(x)
        denominator = 0  # 分母
        numerator = 0  # 分子

        for i in range(n):
            numerator += (x[i] - np.mean(x)) * (y[i] - np.mean(y))
            denominator += (x[i] - np.mean(x)) ** 2

        line_K = numerator / float(denominator)  # 斜率
        line_D = np.mean(y) / float(np.mean(x))  # 截距

        return line_K, line_D


    def learning_face(self,img):

        # 眉毛直线拟合数据缓冲
        line_brow_x = []
        line_brow_y = []

        # 定义每个指标的权重
        mouth_higth_weigth = 0.3
        mouth_width_weigth = 0.3
        brow_hight_weigth  = 0
        brow_width_weigth  = 0.1
        eye_hight_weigth   = 0.3

        # 综合指标
        self.overall = 0

        #cap = cv2.VideoCapture(0)
        
            #_,img = cap.read()
            # 图片所在路径
        img = cv2.imread(img)
        # 取灰度，因为detector方法需要参数为灰度图像
        img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        # 使用特征点表示人脸数据,参数1？
        self.face = self.detector(img_gray,1)
        # print("识别人脸数：",len(self.face))

        if (len(self.face) > 0):

            for k,d in enumerate(self.face):
                # 用矩形框出人脸,并输出识别框的参数
                cv2.rectangle(img,(d.left(),d.top()),(d.right(),d.bottom()),(255,255,255))

                # get_frontal_face_detector得到的面部识别框都是正方形
                self.face_width = d.right()-d.left()
                #print("第",(k+1),"个面部识别框的边长：",self.face_width)

                # 使用预测器得到68点数据信息
                shape = self.predictor(img,d)
                """
                想要的全部特征点全部保存在了shape，
                d是dlib.get_frontal_face_detector()，里面保存着人脸检测矩形的左上和右下坐标
                shape.part(i)是第i个特征点
                """
                # 给人脸打上标签，用来区分多张人脸
                cv2.putText(img,str((k+1)),(d.left(), d.top()),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255))

                # 标出68个点的位置
                for i in range(68):
                    cv2.circle(img,(shape.part(i).x,shape.part(i).y),4,(0,255,0),-1,8)
                    cv2.putText(img,str(i),(shape.part(i).x,shape.part(i).y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255))

                # 分析任意n点的位置关系来作为表情识别的依据
                mouth_width = (shape.part(54).x-shape.part(48).x)/self.face_width     # 嘴巴咧开程度
                mouth_higth = (shape.part(66).y-shape.part(62).y)/self.face_width     # 嘴巴张开程度
                #print("嘴巴宽度与识别框宽度之比：",mouth_width_arv)
                #print("嘴巴高度与识别框高度之比：",mouth_higth_arv)

                # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                brow_sum = 0    # 高度之和
                frown_sum = 0   # 两边眉毛距离之和
                for j in range(17,21):
                    brow_sum+=  (shape.part(j).y - d.top()) + (shape.part(j+5).y - d.top())
                    frown_sum+= shape.part(j+5).x - shape.part(j).x
                    line_brow_x.append(shape.part(j).x)
                    line_brow_y.append(shape.part(j).y)

                #self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                tempx = np.array(line_brow_x)
                tempy = np.array(line_brow_y)
                z1 = np.polyfit(tempx,tempy,1)      # 拟合成一次直线
                self.brow_k = -round(z1[0],3)       # 拟合出曲线的斜率和实际眉毛的倾斜方向是相反的

                brow_hight = (brow_sum/10)/self.face_width       # 眉毛高度占比
                brow_width = (frown_sum/5)/self.face_width       # 眉毛距离占比
                #print("眉毛高度与识别框高度之比：",round(brow_arv/self.face_width,3))
                #print("眉毛间距与识别框高度之比：",round(frown_arv/self.face_width,3))

                # 眼睛睁开程度
                eye_sum = (shape.part(41).y-shape.part(37).y+shape.part(40).y-shape.part(38).y +
                            shape.part(47).y-shape.part(43).y+shape.part(46).y-shape.part(44).y)
                eye_hight = (eye_sum/4)/self.face_width
                #print("眼睛睁开距离与识别框高度之比：",round(eye_open/self.face_width,3))

                # 分情况讨论
                # 张嘴，可能是开心或者惊讶
                if round(mouth_higth >= 0.1):
                    if eye_hight >= 0.05:
                        cv2.putText(img, "amazing", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)
                    else:
                        cv2.putText(img, "happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)

                # 没有张嘴，可能是正常和生气
                else:
                    if self.brow_k <= -0.1:
                        cv2.putText(img, "angry", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)
                    else:
                        cv2.putText(img, "no emotion", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)

                # 显示一下处理的图片，然后销毁窗口
            #cv2.imshow('face',img)
            #cv2.waitKey(5000)
            cv2.imwrite("temp.png",img) 

        #else:
            #print("未检测到人脸数据...")
'''
    def input_image(self,image):
        cap = cv2.VideoCapture(0)
        _,img = cap.read()
'''

if __name__ == '__main__':

    face = face_emotion()
    face.learning_face()
