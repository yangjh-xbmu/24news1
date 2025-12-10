export type ProfessionalMap = Record<string, string[]>;

export const defaultProfessionMap: ProfessionalMap = {
  "新闻传播学类": ["新闻学", "传播学", "广播电视学", "广告学", "编辑出版学", "网络与新媒体", "数字出版"],
  "计算机类": ["计算机科学与技术", "软件工程", "网络工程", "信息安全", "物联网工程", "数字媒体技术", "智能科学与技术", "空间信息与数字技术", "电子与计算机工程"],
  "中国语言文学类": ["汉语言文学", "汉语言", "汉语国际教育", "中国少数民族语言文学", "古典文献学"],
  "法学类": ["法学", "知识产权", "监狱学"],
  "经济学类": ["经济学", "经济统计学", "国民经济管理", "资源与环境经济学", "商务经济学", "能源经济学"],
  "财政学类": ["财政学", "税收学"],
  "金融学类": ["金融学", "金融工程", "保险学", "投资学", "金融数学", "信用管理", "经济与金融"],
  "工商管理类": ["工商管理", "市场营销", "会计学", "财务管理", "国际商务", "人力资源管理", "审计学", "资产评估", "物业管理", "文化产业管理"],
  "公共管理类": ["公共事业管理", "行政管理", "劳动与社会保障", "土地资源管理", "城市管理"],
  "电子信息类": ["电子信息工程", "电子科学与技术", "通信工程", "微电子科学与工程", "光电信息科学与工程", "信息工程"],
};

/**
 * 模糊匹配核心逻辑
 * @param postRequirement 岗位要求的专业（单元格文本）
 * @param userQuery 用户输入的筛选关键词
 * @param map 专业类别映射表
 * @returns 是否匹配
 */
export const fuzzyMatch = (
  postRequirement: string,
  userQuery: string,
  map: ProfessionalMap = defaultProfessionMap
): boolean => {
  if (!userQuery || !userQuery.trim()) return true; // 空查询默认匹配所有
  if (!postRequirement) return false; // 有查询但无要求，不匹配（或者根据业务逻辑，空要求代表不限？）
  // 通常公考职位表中，"不限"会明确写出，或者空着。如果空着代表不限，则应返回True。
  // 但这里FR2.3描述的是“筛选出...的岗位”，暗示是正向匹配。
  // 如果单元格为空，且用户搜具体专业，通常认为不匹配（除非用户搜“不限”）。
  // 让我们假设空单元格不匹配任何具体专业查询。

  // 1. 关键词切分
  // 支持中文/英文逗号、分号、顿号、空格
  const separators = /[;；,，、\s]+/;
  const keywords = userQuery.split(separators).filter(k => k.trim() !== '');

  // 预处理岗位要求文本：统一转小写（虽然中文无大小写，但可能有英文缩写）
  const normalizedPostReq = postRequirement.toLowerCase();

  return keywords.some(keyword => {
    const normalizedKeyword = keyword.trim().toLowerCase();
    if (!normalizedKeyword) return false;

    // 方向A：岗位专业包含用户关键词
    // 例如：岗位="新闻传播学类"，关键词="新闻" -> 包含
    if (normalizedPostReq.includes(normalizedKeyword)) {
      return true;
    }

    // 方向B：用户关键词包含岗位专业类别（通过映射表）
    // 即：用户搜“新闻学”（Sub），岗位要“新闻传播学类”（Super）
    // 逻辑：查找所有包含 normalizedKeyword 的 SuperKey
    const matchedSuperCategories = Object.keys(map).filter(superCat => {
      // 检查映射表中的子类是否包含用户关键词（全等匹配通常更准确，但考虑到用户输入可能不完整，
      // 映射表里的子类通常是标准名称。用户输入“新闻学”，映射表里有“新闻学”。
      // 如果用户输入“新闻”，映射表里有“新闻学”，算不算？
      // 需求描述：用户输入具体专业（如“新闻学”）。
      // 建议：映射表匹配使用精确匹配，或者如果映射表里的词包含用户输入词？
      // 简单起见，检查映射表数组中是否包含用户输入词。
      const subCategories = map[superCat];
      return subCategories.some(sub => sub === keyword.trim() || sub.toLowerCase() === normalizedKeyword);
    });

    // 如果找到对应的上级类别，检查岗位要求是否包含这些上级类别
    return matchedSuperCategories.some(superCat => 
      normalizedPostReq.includes(superCat.toLowerCase())
    );
  });
};
