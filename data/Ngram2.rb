# -*- coding: utf-8 -*-
class String
  def ngram n
    characters = self.split(//u)
    return [self] if characters.size <= n
    return 0.upto(characters.size-n).collect do |i|
      characters[i, n].join
    end
  end
end

p "テキスト検索を行う場合".ngram(2)
