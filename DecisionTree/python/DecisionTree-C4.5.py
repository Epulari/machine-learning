from math import log
import operator

def createDataSet1():
    """
    创造示例数据/读取数据
    @param dataSet: 数据集
    @return dataSet labels：数据集 特征集
    """
    # 数据集
    dataSet = [('青年', '否', '否', '一般', '不同意'),
               ('青年', '否', '否', '好', '不同意'),
               ('青年', '是', '否', '好', '同意'),
               ('青年', '是', '是', '一般', '同意'),
               ('青年', '否', '否', '一般', '不同意'),
               ('中年', '否', '否', '一般', '不同意'),
               ('中年', '否', '否', '好', '不同意'),
               ('中年', '是', '是', '好', '同意'),
               ('中年', '否', '是', '非常好', '同意'),
               ('中年', '否', '是', '非常好', '同意'),
               ('老年', '否', '是', '非常好', '同意'),
               ('老年', '否', '是', '好', '同意'),
               ('老年', '是', '否', '好', '同意'),
               ('老年', '是', '否', '非常好', '同意'),
               ('老年', '否', '否', '一般', '不同意')]
    # 特征集
    labels = ['年龄', '有工作', '有房子', '信贷情况']
    return dataSet,labels

def calcShannonEnt(dataSet):
    """
    计算数据的熵(entropy)
    @param dataSet: 数据集
    @return shannonEnt: 数据集的熵
    """
    numEntries = len(dataSet)  # 数据条数
    # 循环判断每个样本的类别，统计每个类别的样本总数
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]  # 当前样本类型
        # 统计每个样本类型的数量
        try:
        	labelCounts[currentLabel] += 1
        except KeyError:
        	labelCounts[currentLabel] = 1
    # 根据公式计算香浓熵
    shannonEnt = 0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataSet, index, value):
    """
    划分数据集，提取含有某个特征的某个属性的所有数据
    @param dataSet: 数据集
    @param index: 属性值所对应的特征列
    @param value: 某个属性值
    @return retDataSet: 含有某个特征的某个属性的数据集
    """
    retDataSet = []
    for featVec in dataSet:
        # 如果该样本该特征的属性值等于传入的属性值，则去掉该属性然后放入数据集中
        if featVec[index] == value:
            reducedFeatVec = featVec[:index] + featVec[index+1:] # 去掉该属性的当前样本
            retDataSet.append(reducedFeatVec) # append向末尾追加一个新元素，新元素在元素中格式不变，如数组作为一个值在元素中存在
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    """
    选择最优特征
    @param dataSet: 数据集
    @return bestFeature: 最优特征所在列
    """
    numFeatures = len(dataSet[0]) - 1 # 特征总数
    if numFeatures == 1:  # 当只有一个特征时
        return 0
    baseEntropy = calcShannonEnt(dataSet)  # 数据集的熵
    bestInfoGainRatio = 0 # 最佳信息增益比
    bestFeature = -1 # 最优特征所在列
    for i in range(numFeatures): # range(5) 代表从0到5，不包括5
        uniqueVals = set(example[i] for example in dataSet) # 去重，每个属性值唯一
        newEntropy = 0 # 定义按特征分类后的熵
        feaEntropy = 0 # 定义特征的值的熵
        # 依次计算每个特征的值的熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value) # 根据该特征属性值分的类
                                                       # 参数：原数据、循环次数(当前属性值所在列)、当前属性值
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
            feaEntropy -= prob * log(prob, 2)
        infoGainRatio = (baseEntropy - newEntropy) / feaEntropy   # 信息增益比
        if (infoGainRatio > bestInfoGainRatio):   # 或infoGainRatio > bestInfoGainRatio若按某特征划分后，熵值减少的最大，则此特征为最优分类特征
            bestInfoGainRatio = infoGainRatio
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    """
    对最后一个特征分类，出现次数最多的类即为该属性类别，比如：最后分类为2男1女，则判定为男
    @param classList: 数据集，也是类别集
    @return sortedClassCount[0][0]: 该属性的类别
    """
    classCount = {}
    # 计算每个类别出现次数
    for vote in classList:
        try:
            classCount[vote] += 1
        except KeyError:
            classCount[vote] = 1
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True) # 出现次数最多的类别在首位
                                                    # 对第1个参数，按照参数的第1个域来进行排序（第2个参数），然后反序（第3个参数）
    return sortedClassCount[0][0] # 该属性的类别

def createTree(dataSet,labels):
    """
    对最后一个特征分类，按分类后类别数量排序，比如：最后分类为2男1女，则判定为男
    @param dataSet: 数据集
    @param labels: 特征集
    @return myTree: 决策树
    """
    classList = [example[-1] for example in dataSet]  # 获取每行数据的最后一个值，即每行数据的类别
    # 当数据集只有一个类别
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 当数据集只剩一列（即类别），即根据最后一个特征分类
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    # 其他情况
    bestFeat = chooseBestFeatureToSplit(dataSet) # 选择最优特征（所在列）
    bestFeatLabel = labels[bestFeat] # 最优特征
    del(labels[bestFeat]) # 从特征集中删除当前最优特征
    uniqueVals = set(example[bestFeat] for example in dataSet) # 选出最优特征对应属性的唯一值
    myTree = {bestFeatLabel:{}} # 分类结 果以字典形式保存
    for value in uniqueVals:
        subLabels = labels[:] # 深拷贝，拷贝后的值与原值无关（普通复制为浅拷贝，对原值或拷贝后的值的改变互相影响）
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels) # 递归调用创建决策树
    return myTree


if __name__ == '__main__':
	dataSet, labels = createDataSet1()  # 创造示列数据
	print(createTree(dataSet, labels))  # 输出决策树模型结果