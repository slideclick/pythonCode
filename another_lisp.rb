# 30 minutes Lisp in Ruby
# Hong Minhee <http://dahlia.kr/>
#
# This Lisp implementation does not provide a s-expression reader.
# Instead, it uses Ruby syntax like following code:
#
#     [:def, :factorial,
#       [:lambda, [:n],
#         [:if, [:"=", :n, 1],
#               1,
#               [:*, :n, [:factorial, [:-, :n, 1]]]]]]
#
# Enter the REPL:
#
#    $ ruby lisp.rb
#    >>> 
#
require 'rational'

module Lisp
  SPECIAL_FORMS = {:def => lambda do |name, value|
                             value = value.analyze_form
                             lambda do |env|
                               val = value.call(env)
                               env[name] = val
                               if val.is_a?(Lambda) && val.name
                                 val.name = name 
                               end
                               val
                             end
                           end,
                   :lambda => lambda do |params, body|
                                eval_body = body.analyze_form
                                lambda do |env|
                                  Lambda.new(env, params, eval_body)
                                end
                              end,
                   :quote => lambda do |form|
                               lambda {|env| form }
                             end,
                   :if => lambda do |cond, trueval, falseval|
                            cond = cond.analyze_form
                            trueval = trueval.analyze_form
                            falseval = falseval.analyze_form
                            lambda do |env|
                              val = cond.call(env) ? trueval : falseval
                              val.call(env)
                            end
                          end}

  class ::Symbol
    def analyze_form
      lambda {|env| env[self] }
    end
  end

  class ::Numeric
    def analyze_form
      lambda {|env| self }
    end
  end

  class ::String
    def analyze_form
      lambda {|env| self }
    end
  end

  class ::Array
    def analyze_form
      if SPECIAL_FORMS.include?(self.first)
        return SPECIAL_FORMS[self.first].call(*self[1..-1])
      end
      list = self.map {|form| form.analyze_form }
      lambda do |env|
        lst = list.map {|analyze| analyze.call(env) }
        lst.first.call(*lst[1..-1])
      end
    end
  end

  class Quote
    attr_accessor :form

    def initialize(form)
      self.form = form
    end

    def analyze_form
      lambda {|env| self.form }
    end
  end

  class Lambda
    attr_accessor :environment, :parameters, :body, :name

    def initialize(environment, parameters, body, name = nil)
      self.environment = environment
      self.parameters = parameters
      self.body = body
      self.name = name
    end

    def call(*args)
      env = Environment[self.parameters.zip(args)]
      env.superenv = self.environment
      body.call(env)
    end

    def inspect
      self.name ? "#<Lisp::Lambda #{self.name}>" : "#<Lisp::Lambda>"
    end
  end

  class Environment < Hash
    attr_accessor :superenv

    def initialize(superenv = nil)
      self.superenv = superenv
    end

    def [](key)
      include?(key, true) ? super(key) : self.superenv && self.superenv[key]
    end

    def empty?
      super && (!self.superenv || self.superenv.empty?)
    end

    def include?(key, without_superenv = false)
      result = super(key)
      unless without_superenv
        result ||= self.superenv && self.superenv.include?(key)
      end
      result
    end

    def has_key?(key, without_superenv = false)
      include?(key, without_superenv)
    end

    def key?(key, without_superenv = false)
      include?(key, without_superenv)
    end

    def keys(without_superenv = false)
      without_superenv ? super : (super + self.superenv.keys).uniq
    end

    def evaluate(form)
      form.analyze_form.call(self)
    end
  end

  module Runtime
    def initialize_environment
      Environment[:car, lambda {|lst| lst.empty? ? nil : lst.first },
                  :cdr, lambda {|lst| lst.empty? ? nil : lst[1..-1] },
                  :null, lambda { nil },
                  :and, lambda {|*args| args.all? },
                  :or, lambda {|*args| args.any? },
                  :list, lambda {|*args| args },
                  :append, lambda {|a, b| a + b },
                  :apply, lambda {|proc, args| proc.call(*args) },
                  :eval, lambda {|form, env| env.evaluate(form) },
                  :+, lambda {|*args| args.inject(0) {|x, y| x + y } },
                  :-, lambda do |v, *args|
                        args.empty? ? -v : args.inject(v) {|x, y| x - y }
                      end,
                  :*, lambda {|*args| args.inject(1) {|x, y| x * y } },
                  :/, method(:Rational),
                  :div, lambda {|*args| args.inject(1.0) {|x, y| x / y } },
                  :%, lambda {|*args| args.inject(1) {|x, y| x % y } },
                  :"=", lambda {|a, b| a == b},
                  :>, lambda {|a, b| a > b},
                  :<, lambda {|a, b| a < b},
                  :>=, lambda {|a, b| a >= b},
                  :<=, lambda {|a, b| a <= b},
                  :string, lambda {|*args| args.map {|x| x.to_s }.join },
                  :hash, lambda {|*args| Hash[*args] },
                  :symbol?, lambda {|v| v.isa?(Symbol) },
                  :number?, lambda {|v| v.isa?(Numeric) },
                  :string?, lambda {|v| v.isa?(String) },
                  :list?, lambda {|v| v.isa?(Array) },
                  :quote?, lambda {|v| v.isa?(Quote) },
                  :function?, lambda {|v| v.respond_to?(:call) },
                  :hash?, lambda {|v| v.isa?(Hash) }]
    end
  end
end

class Lisp::REPL
  include Lisp::Runtime
  attr_accessor :environment

  def initialize
    self.environment = initialize_environment()
  end

  def loop
    require 'readline'
    while buf = Readline.readline('>>> ', true)
      begin
        form = eval(buf)
        result = self.environment.evaluate(form)
        puts "==> #{result.inspect}"
      rescue Exception => e
        puts "!!!      #{e.backtrace.first} #{e} (#{e.class.name})"
        for stack in e.backtrace[1..-1]
          puts "    from #{stack}"
        end
      end
    end
  end
end

if __FILE__ == $0
  repl = Lisp::REPL.new
  repl.loop()
end
