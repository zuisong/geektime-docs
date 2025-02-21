你好，我是王健伟。

上节课我们针对串的KMP模式匹配算法配以了大量的图形进行了非常仔细的观察，而观察的目的，就是为了这节课代码的实现。

串的KMP模式匹配算法实现代码并不多，但只有你学好了上节课的内容，对该算法有详细的理解，才能理解本节这样写代码的含义。

## KMP模式匹配算法实现代码

KMP模式匹配算法实现代码各式各样，有些实现方法虽然简洁，但并不好理解，我这里先以比较容易理解的方式进行代码实现。你可以先仔细读一遍。

```plain
//求本串的next数组
void getNextArray( int next[])
{
	//next数组下标为0和为1的元素值固定为0和1。其实next[0]里的值并没有用到
	if (length < 1)
		return;
	
	//next数组的前两个元素肯定是0和1
	if (length == 1) //只有一个字符
	{
		next[0] = 0;
		return;
	}
		
	next[0] = 0;
	next[1] = 1;
	if (length == 2) //只有二个字符
	{
		return;
	}
		
	//至少三个字符
	int nextarry_idx = 2; //当前要处理的next数组下标
	int max_pub_zhui = 0; //max_pub_zhui：最大公共前后缀包含的字符数量
	
	//循环的目的是给next数组赋值
	while (nextarry_idx < length) 
	{
		int left_RMC_count = nextarry_idx; //left_RMC_count：如果当前字符与主串的字符不匹配，当前字符左侧有多少个字符
		int max_pub_zhui = left_RMC_count - 1; //max_pub_zhui：最大公共前后缀包含的字符数量
		
		int start1idx = 0;
		int start2idx = left_RMC_count - max_pub_zhui;
		
		int xhtimes = max_pub_zhui; //循环次数
		
		//本循环的目的是获取最长公共前后缀长度，代码写法无固定方式，选择自己容易理解的方式写即可
		while (xhtimes > 0)
		{
			if (ch[start1idx] != ch[start2idx])
			{
				max_pub_zhui--;
				start1idx = 0;
				start2idx = left_RMC_count - max_pub_zhui;
				xhtimes = max_pub_zhui;
				continue; //要回去重新循环
			}
			else
			{
				start1idx++;
				start2idx++;
			}
			xhtimes--;
		} //end while (xhtimes > 0)
		next[nextarry_idx] = max_pub_zhui + 1; //如果公共前后缀长度为n，那么就需要用子串的第n+1个字符与主串当前位做比较。
		nextarry_idx++;
	} //end while
	return;
}
	
//KMP模式匹配算法接口，返回子串中第一个字符在主串中的下标，如果没找到子串，则返回-1
//next：下一步数组（前缀表/前缀数组）
//pos：从主串的什么位置开始匹配子串，默认从位置0开始匹配子串
int StrKMPIndex(const MySString& substr, int next[], int pos = 0)
{
	if (length < substr.length) //主串还没子串长，那不可能找到
		return -1;		
	
	int point1 = pos; //指向主串
	int point2 = 0;  //指向子串
	
	while (ch[point1] != '\0' && substr.ch[point2] != '\0')
	{
		if (ch[point1] == substr.ch[point2])
		{
			//两个指针都向后走
			point1++;
			point2++;
		}
		else //两者不同
		{
			//point1和point2两个指针的处理
			
			if (point2 == 0) //下标0号位置子串的字符如果与主串字符不匹配则后续就要用子串的第1个字符（字符a）与主串下一位（1号下标位）字符做比较 
			{
				point1++; //主串指针指向下一位
			}
			else
			{
				//走到这个分支的，主串指针point1不用动，只动子串指针point2
				point2 = next[point2] - 1; //第这些个子串中的字符与主串当前位字符做比较
			}
		}
	}//end while
	
	if (substr.ch[point2] == '\0')
	{
		//找到了子串
		return point1 - point2;
	}
	return -1;
}
```