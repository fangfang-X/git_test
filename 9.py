# -*- coding: utf-8 -*-
###
def plot_activation(img):
    # 使用预训练模型对图像进行预测
    pred = model.predict(img[np.newaxis, :, :, :])
    # 获取预测结果的类别
    pred_class = np.argmax(pred)

    # 获取模型最后一层的权重
    weights = model.layers[-1].get_weights()[0]
    # 根据预测类别选择相应的权重
    class_weights = weights[:, pred_class]

    # 定义一个新模型，输入为原模型的输入，输出为指定中间层的输出
    intermediate = Model(model.input,model.get_layer("block5_conv3").output)
    # 使用新模型获取输入图像在指定中间层的输出
    conv_output = intermediate.predict(img[np.newaxis, :, :, :])
    # 去除输出中的单维度
    conv_output = np.squeeze(conv_output)

    # 计算缩放因子，以便将激活图的尺寸调整为与输入图像相同
    h = int(img.shape[0] / conv_output.shape[0])
    w = int(img.shape[1] / conv_output.shape[1])
    # 使用插值将激活图的尺寸调整为与输入图像相同
    act_maps = sp.ndimage.zoom(conv_output, (h, w, 1), order=1)

    # 将激活图与权重相乘并重塑为与输入图像相同的形状
    out = np.dot(act_maps.reshape((img.shape[0] * img.shape[1], 512)),
                 class_weights).reshape(img.shape[0], img.shape[1])

    # 显示输入图像
    plt.imshow(img.astype('float32').reshape(img.shape[0],
                                             img.shape[1], 3))
    # 叠加显示激活图，并使用热力图的颜色映射
    plt.imshow(out, cmap='jet', alpha=0.35)
    # 设置图像标题，根据预测类别判断是否有裂纹
    plt.title('Crack' if pred_class == 1 else 'No Crack')
