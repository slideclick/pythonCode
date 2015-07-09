using System;
//using System.Collections.Generic;
//using System.Linq;
using System.Text;
using weiss.Collections.Generic;

namespace GenerateAST
{

    public class Evaluator
    {
        private string post;
        BinaryTree<char> ast;
        public string GetPost(){ return post;}
        public void GetPre() { 
            ast.PrintPreOrder();
            Console.WriteLine(); 
        }
        public string GetSexpr() { return "GetSexpr"; }
        public Evaluator(string s)
        {
            post = s;
            
            Stack<BinaryTree<char>> opStack = new Stack<BinaryTree<char>> ();

            foreach (char c in s)
            {
                if ((c == '+') ||(c == '*'))
                {
                    BinaryTree<char> op = new BinaryTree<char>();
                    BinaryTree<char> or = opStack.Pop();
                    BinaryTree<char> ol = opStack.Pop();
                    op.Merge(c, ol,or);
                    opStack.Push(op);
                }
                else if (c == ' ')
                {
                    continue;
                }
                else
                {
                    BinaryTree<char> o1 = new BinaryTree<char>(c);
                    opStack.Push(o1);
                }
            }

            ast = opStack.Pop();


           
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
                    string str;

        try
        {
            //Console.WriteLine( "Enter expressions, one per line:" );
            while( ( str = Console.ReadLine( ) ) != null )
            {

                Evaluator ev = new Evaluator(str);
                ev.GetPre();

            }
            //Console.ReadKey ();
        }


        catch (Exception e) { Console.Error.WriteLine(e); 
            //throw e; 
        }

        }

    }
    
}
