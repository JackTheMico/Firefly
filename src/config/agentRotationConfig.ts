// ZZZ Daily Featured Agent Rotation Configuration

export interface AgentOnDuty {
	id: string;
	name: string;
	faction: string;
	avatarAnimated: string;
	avatarStatic: string;
	badgeText: string;
	quote: string;
}

export const AGENTS_POOL: AgentOnDuty[] = [
	{
		id: "ellen",
		name: "艾莲·乔",
		faction: "维多利亚家政",
		avatarAnimated: "/assets/images/agents/ellen.webp",
		avatarStatic: "/assets/images/agents/ellen-static.png",
		badgeText: "今日值勤: 艾莲·乔 // 维多利亚家政",
		quote: "麻烦死了...速战速决吧，我还赶着去吃甜点呢。",
	},
	{
		id: "anby",
		name: "安比·德玛拉",
		faction: "狡兔屋",
		avatarAnimated: "/assets/images/agents/anby.webp",
		avatarStatic: "/assets/images/agents/anby-static.png",
		badgeText: "今日值勤: 安比·德玛拉 // 狡兔屋",
		quote: "汉堡和电影是必需品。委托，已经确认接收。",
	},
	{
		id: "jane",
		name: "简·杜",
		faction: "刑侦特勤组",
		avatarAnimated: "/assets/images/agents/jane.webp",
		avatarStatic: "/assets/images/agents/jane-static.png",
		badgeText: "今日值勤: 简·杜 // 刑侦特勤组",
		quote: "放轻松点，绳匠。跟着我的节奏，绝对不会被抓到的~",
	},
	{
		id: "nicole",
		name: "妮可·德玛拉",
		faction: "狡兔屋",
		avatarAnimated: "/assets/images/agents/nicole.webp",
		avatarStatic: "/assets/images/agents/nicole-static.png",
		badgeText: "今日值勤: 妮可·德玛拉 // 狡兔屋",
		quote: "狡兔屋全员待命！这次的委托报酬可不能再打折了！",
	},
	{
		id: "zhuyuan",
		name: "朱鸢",
		faction: "刑侦特勤组",
		avatarAnimated: "/assets/images/agents/zhuyuan.webp",
		avatarStatic: "/assets/images/agents/zhuyuan-static.png",
		badgeText: "今日值勤: 朱鸢 // 刑侦特勤组",
		quote: "治安局刑侦特勤组朱鸢，随时准备应对空洞灾害与突发事态！",
	},
];

/**
 * Returns the agent on duty based on the current date (daily deterministic rotation).
 */
export function getAgentOnDuty(date: Date = new Date()): AgentOnDuty {
	const startOfYear = new Date(date.getFullYear(), 0, 0);
	const diff =
		date.getTime() -
		startOfYear.getTime() +
		(startOfYear.getTimezoneOffset() - date.getTimezoneOffset()) * 60 * 1000;
	const oneDay = 1000 * 60 * 60 * 24;
	const dayOfYear = Math.floor(diff / oneDay);
	const index = Math.abs(dayOfYear) % AGENTS_POOL.length;
	return AGENTS_POOL[index];
}
