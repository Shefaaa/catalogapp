from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///bookcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Shefaa", email="shefaa.it@gmail.com")
session.add(User1)
session.commit()

# Menu for UrbanBurger
category1 = Category(name="Arts and Music")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id=1, title="Photography", description="A classic reference work now fully revised for a second edition, Photography combines how-to information with inspiring examples to illustrate techniques that readers can immediately apply to their own work, whether in color or black and white. An all-new chapter on digital photography, plus an in-depth look at the world of commercial photography, make this edition a must-have primer and reference for beginning through intermediate students, amateurs, and aspiring professionals.",
                         category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, title="Making Faces", description="Americas preeminent makeup artist shares his secrets, explaining not only the basics of makeup application and technique but also how to use the fundamentals to create a wide range of different looks. 200 color photos & sketches.",
                         category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, title="Zoom", description="As seen on the SERIAL podcast, season 2, episode 1 Dustwun Open this wordless book and zoom from a farm to a ship to a city street to a desert island. But if you think you know where you are, guess again. For nothing is ever as it seems in Istvan Banyai's sleek, mysterious landscapes of pictures within pictures, which will tease and delight readers of all ages. This book has the fascinating appeal of such works of visual trickery as the Waldo and Magic Eye books. -- Kirkus Reviews Ingenious.-- The Horn Book",
                         category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, title="Artist's Manual", description="A veritable bible for beginners as well as an invaluable reference for accomplished artists, The Artist's Manual is a hands-on guide to hundreds of techniques for painting and drawing. For anyone who has ever had the urge to create art, this easy-to-use manual clearly explains the artist's essential tools and materials -- how to choose them, how to use them, and how to care for them. Packed with information on myriad techniques, from color use and composition to subject choice, and including tips from the professionals, here's everything painters and illustrators need to begin, develop, and perfect their craft. Over 500 color photographs, 200 original works of art, and an extensive list of suppliers complete the most comprehensive, inspirational, and affordable artists' instruction book available today.",
                         category=category1)

session.add(categoryItem4)
session.commit()


# Menu for Super Stir Fry
category2 = Category(name="Business")

session.add(category2)
session.commit()


categoryItem1 = CategoryItem(user_id=1, title="The Story of Success", description="In this stunning new book, Malcolm Gladwell takes us on an intellectual journey through the world of outliers--the best and the brightest, the most famous and the most successful. He asks the question: what makes high-achievers different? His answer is that we pay too much attention to what successful people are like, and too little attention to where they are from: that is, their culture, their family, their generation, and the idiosyncratic experiences of their upbringing. Along the way he explains the secrets of software billionaires, what it takes to be a great soccer player, why Asians are good at math, and what made the Beatles the greatest rock band. Brilliant and entertaining, Outliers is a landmark work that will simultaneously delight and illuminate.",
                         category=category2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, title="Think and Grow Rich", description="Think and Grow Rich - Over 80 Million Copies Sold This edition of Napoleon Hill'sClassic T hink and Grow Rich is a reproduction of Napoleon Hill's personal copy of the first edition, the ONLY original version recommended by The Napoleon Hill Foundation, originally printed in March of 1937. The most famous of all teachers of success spent a fortune and the better part of a lifetime of effort to produce the Law of Success philosophy that forms the basis of his books and that is so powerfully summarized and explained for the general public in this book. In Think and Grow Rich , Hill draws on stories of Andrew Carnegie, Thomas Edison, Henry Ford, and other millionaires of his generation to illustrate his principles. This book will teach you the secrets that could bring you a fortune. It will show you not only what to do but how to do it. Once you learn and apply the simple, basic techniques revealed here, you will have mastered the secret of true and lasting success. Money and material things are essential for freedom of body and mind, but there are some who will feel that the greatest of all riches can be evaluated only in terms of lasting friendships, loving family relationships, understanding between business associates, and introspective harmony which brings one true peace of mind All who read, understand, and apply this philosophy will be better prepared to attract and enjoy these spiritual values. BE PREPARED When you expose yourself to the influence of this philosophy, you may experience a CHANGED LIFE which can help you negotiate your way through life with harmony and understanding and prepare you for the accumulation of abundant material riches.",
                         category=category2)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, title="Zoom", description="As seen on the SERIAL podcast, season 2, episode 1 Dustwun Open this wordless book and zoom from a farm to a ship to a city street to a desert island. But if you think you know where you are, guess again. For nothing is ever as it seems in Istvan Banyai's sleek, mysterious landscapes of pictures within pictures, which will tease and delight readers of all ages. This book has the fascinating appeal of such works of visual trickery as the Waldo and Magic Eye books. -- Kirkus Reviews Ingenious.-- The Horn Book",
                         category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, title="Artist's Manual", description="A veritable bible for beginners as well as an invaluable reference for accomplished artists, The Artist's Manual is a hands-on guide to hundreds of techniques for painting and drawing. For anyone who has ever had the urge to create art, this easy-to-use manual clearly explains the artist's essential tools and materials -- how to choose them, how to use them, and how to care for them. Packed with information on myriad techniques, from color use and composition to subject choice, and including tips from the professionals, here's everything painters and illustrators need to begin, develop, and perfect their craft. Over 500 color photographs, 200 original works of art, and an extensive list of suppliers complete the most comprehensive, inspirational, and affordable artists' instruction book available today.",
                         category=category1)

session.add(categoryItem4)
session.commit()


# Menu for Panda Garden
category3 = Category(name="Entertainment")

session.add(category3)
session.commit()


categoryItem1 = CategoryItem(user_id=1, title="Great Expectations", description="Great Expectations is at once a superbly constructed novel of spellbinding mastery and a profound examination of moral values. Here, some of Dickens most memorable characters come to play their part in a story whose title itself reflects the deep irony that shaped Dickens searching reappraisal of the Victorian middle class.  Great Expectations has over 1.8 million Signet Classic copies in print A new major motion picture release ofGreat Expectations is due for release starring Ethan Hawke, Gwyneth Paltrow,and Robert DeNiro *Charles Dickens is also the author of the popular Signet Classic titles: A Christmas Carol, David Copperfield, Hard Times, Oliver Twist, and A Tale of Two Cities Course Adoption: High School: Senior High School Literature College: 19th Century English Literature",
                         category=category3)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, title="Hop on Pop", description="This classic Beginner Book makes an ideal gift for Seuss fans and is an especially good way to show Pop some love Loved by generations, this simplest Seuss for youngest use is a Beginner Book classic. See Red and Ned and Ted and Ed in a bed. And giggle as Pat sits on a hat and on a cat and on a bat . . . but a cactus? Pat must NOT sit on that This classic Beginner Book makes an ideal gift for Seuss fans and is an especially good way to show Pop some love on Fathers Day Originally created by Dr. Seuss, Beginner Books encourage children to read all by themselves, with simple words and illustrations that give clues to their meaning.",
                         category=category3)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, title="The Ugly Truth", description="Greg Heffley has always been in a hurry to grow up. But is getting older really all it is cracked up to be? Greg suddenly finds himself dealing with the pressures of boy girl parties, increased responsibilities, and even the awkward changes that come with getting older all without his best friend, Rowley, at his side. Can Greg make it through on his own? Or will he have to face the ugly truth?",
                         category=category3)

session.add(categoryItem3)
session.commit()





print "added menu items"
