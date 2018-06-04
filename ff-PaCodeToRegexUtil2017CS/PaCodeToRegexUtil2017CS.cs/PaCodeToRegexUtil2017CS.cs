using System;
using System.IO;
using System.Collections;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;

class PaCodeToRegexUtil2017CS{
	private string strWordChars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
	private string[] A_strWriteChars = {" ", "\t", "\r", "\n"};
	private string strSpecialChars = "^$[](){}.*?+|\\";
	private string[] EOP = {"+", "-", "*", "/", "~", "|"}; // +=  -= ....
	private string[] DOP = {"++", "--", "**", "==", "//", "||", "&&", "$$"};
	private string[] A_strStrChars = {"\"", "'"};
	private static char chNull = (char)0;

	private bool isWord   = false;
	private bool isSpec   = false;
	private bool isSpace  = false;
	private bool isString = false;
	private char strChar  = chNull;


	public PaCodeToRegexUtil2017CS(){
		Console.WriteLine("PaCodeToRegexUtil2017CS.cs");
		string[] A_strLines = ReadTextFile( "PaCodeToRegexUtil2017CS.txt" ).Split('\n');
		string splitter = "==============================";
		for(int i = 0, ls = A_strLines.Length; i < ls; i++){
			string strLine = A_strLines[i];
			string sRegEx = ToRegexStringEx( strLine );

			int ls2 = strLine.Length - 1;
			if( ls2 > 0 && strLine[ ls2 ] == '\r' ){
				strLine = strLine.Substring( 0, ls2 );
			}

			Console.WriteLine( splitter );
			Console.WriteLine( strLine );
			Console.WriteLine( sRegEx );
			Match m = Regex.Match( strLine, sRegEx );
			if( m.Success ){
				Console.Write( "[ ");
				Console.Write( m.Value );
				Console.WriteLine(" ]");
			}
			//Console.WriteLine( m.Success );
		}
		//Console.WriteLine( "ToRegexStringEx = " + ToRegexStringEx("for (var i = 0, ls = A_strNoCheckPage.length; i < ls; i++) {") );
	}

	public string ReadTextFile(string file){
		string strContent = null;
		try{
			using(FileStream fs = new FileStream(file, FileMode.Open, FileAccess.Read, FileShare.ReadWrite)){
				using(StreamReader sr = new StreamReader(fs, System.Text.Encoding.UTF8)){
					strContent = sr.ReadToEnd();
				}
			}
		}catch(Exception ex){
			MessageBox.Show("Exception: " + ex.Message);
		}
		return strContent;
	}

	public string ToRegexStringEx(string s){
		if (s == null) return null;
		ArrayList al = new ArrayList();
		int ls = s.Length;
		char pch = chNull; // pch : prev char
		int m_nStart = 0;

		for(int i = 0; i < ls; i++){
			char ch = s[i];

			if( ! this.isString && InSet(ch, this.A_strStrChars) ){
				m_nStart = i;
				this.strChar = ch;
				SetSwitch(4);
			}else{
				if( this.isString ){
					if( ch == this.strChar && pch != '\\' ){
						this.strChar = chNull;
						this.SetSwitch(0);
						al.Add( s.Substring(m_nStart, i + 1 - m_nStart) );
					}
				}else{
					if( InChars(ch, this.strWordChars) ){
						if( ! this.isWord ){
							m_nStart = i;
						}
						this.SetSwitch(2);
					}else{
						if( this.isWord ){
							al.Add( s.Substring(m_nStart, i - m_nStart) );
						}
						if( InSet(ch, this.A_strWriteChars) ){
							this.SetSwitch(0);
						}else{
							if( i < ls - 1){
								char ch2 = s[i + 1];
								string ss = ch.ToString() + ch2.ToString();
								if( InSet(ss, this.DOP ) || ch2 == '=' && InSet(ch, this.EOP) ){
									al.Add( ss );
									i++;
								}else{
									al.Add( ch.ToString() );
								}
							}else{
								al.Add( ch.ToString() );
							}
							this.SetSwitch(1);
						}
					}
				}
			}
			pch = ch;
		}

		StringBuilder sb = new StringBuilder();
		int alc = al.Count;
		//Console.WriteLine("-------------------------");
		for(int i = 0; i < alc; i++){
			string el = (string)al[i];
			//Console.WriteLine( el );
			sb.Append( FixedData( el ) );
			sb.Append( i < (alc - 1) && IsWord(el) && IsWord((string)al[i + 1]) ? "\\s+" : "\\s*");
		}
		//Console.WriteLine("-------------------------");
		return sb.ToString();
	}

	private void SetSwitch(int n){
		this.isSpace  = n==0 ? true : false;
		this.isSpec   = n==1 ? true : false;
		this.isWord   = n==2 ? true : false;
		this.isString = n==4 ? true : false;
	}

	private bool IsWord(string s){
		if(s == null) return false;
		for(int i = 0, l = s.Length; i < l; i++){
			if( ! InChars(s[i], this.strWordChars) ){
				return false;
			}
		}
		return true;
	}

	private string FixedData(string s){
		if(s == null) return null;
		StringBuilder sb = new StringBuilder();
		for(int i = 0, l = s.Length; i < l; i++){
			if( InChars(s[i], this.strSpecialChars) ){
				sb.Append("\\");
			}
			sb.Append(s[i]);
		}
		return sb.ToString();
	}

	public bool InChars(char ch, string _chars){
		int cl = _chars.Length;
		for(int i = 0; i < cl; i++){
			if( ch == _chars[i] ){
				return true;
			}
		}
		return false;
	}

	public bool InSet(char ch, string[] _set){
		return InSet(ch.ToString(), _set);
	}

	public bool InSet(string s, string[] _set){
		int ls = _set.Length;
		for(int i = 0; i < ls; i++){
			if(_set[i] == s){
				return true;
			}
		}
		return false;
	}

	public static void Main(string[] args){
		new PaCodeToRegexUtil2017CS();
	}
}