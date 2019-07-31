from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Movie, User

engine = create_engine('sqlite:///movieswithusers.db')
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

user1 = User(name="Bria", email="email@email.com")
session.add(user1)
session.commit()

# Movies for romantic comedy genre
genre1 = Genre(name="Romantic Comedy", user=user1)

session.add(genre1)
session.commit()

movie1 = Movie(name="27 Dresses", description="Woman who is the very "
               + "definition of \"always the bridesmaid but never the bride\" "
               + "has to deal with being the maid of honor for the wedding of "
               + "her sister to the man she's in love with.", rating="PG-13",
               score="40", genre=genre1, user=user1)

session.add(movie1)
session.commit()

movie2 = Movie(name="Pretty Woman", description="An unlikely pair fall in "
               + "love with each other after she's introduced to life off the "
               + "streets and he learns how to live life carelessly.",
               rating="R", score="62", genre=genre1, user=user1)

session.add(movie2)
session.commit()

movie3 = Movie(name="How to Lose a Guy in 10 Days", description="She makes a "
               + "bet that she can get rid of any man in 10 days. He makes a "
               + "bet that he can make any girl fall in love with him in 10 "
               + "days. Who will win?",
               rating="PG-13", score="42", genre=genre1, user=user1)

session.add(movie3)
session.commit()

movie4 = Movie(name="Hitch", description="Hitch is a successful love doctor "
               + "and certified ladies man, but suddenly he finds himself "
               + "struggling to help his newest client and maintain his "
               + "anonymity all while juggling his own love life.",
               rating="PG-13", score="40", genre=genre1, user=user1)

session.add(movie4)
session.commit()

movie5 = Movie(name="13 Going on 30", description="After suffering "
               + "humiliation by the cool kids in school at her 13th birthday "
               + "party, teenage Jenna wished to be 30, flirty, and thriving. "
               + "Her wished come true, but is it everything she hoped it "
               + "would be?",
               rating="PG-13", score="65", genre=genre1, user=user1)

session.add(movie5)
session.commit()

# Movies for drama genre
genre2 = Genre(name="Drama", user=user1)

session.add(genre2)
session.commit()

movie1 = Movie(name="The Devil Wears Prada", description="Budding journalist "
               + "Andy takes a job as second assistant for the infamous "
               + "Miranda Priestly to jumpstart her writing career.",
               rating="PG-13", score="75", genre=genre2, user=user1)

session.add(movie1)
session.commit()

movie2 = Movie(name="Menace II Society", description="Caine tries to leave "
               + "his violent, gang-affiliated lifestyle behind but escaping "
               + "the hood proves to be harder than planned.",
               rating="R", score="84", genre=genre2, user=user1)

session.add(movie2)
session.commit()

movie3 = Movie(name="The Help", description="A brave author decides to "
               + "examine and share the heart-wrenching tales of the "
               + "courageous, hard working Mississipi maids of the Jim "
               + "Crow south.",
               rating="PG-13", score="76", genre=genre2, user=user1)

session.add(movie3)
session.commit()

movie4 = Movie(name="The Social Network", description="The story of Facebook's"
               + " inception and the lawsuits that followed are depicted in "
               + "this 2010 drama.",
               rating="PG-13", score="95", genre=genre2, user=user1)

session.add(movie4)
session.commit()

movie5 = Movie(name="Creed", description="An unknown boxer tries to make a "
               + "name for himself without using his famous father's name.",
               rating="PG-13", score="95", genre=genre2, user=user1)

session.add(movie5)
session.commit()

# Movies for horror genre
genre3 = Genre(name="Horror", user=user1)

session.add(genre3)
session.commit()

movie1 = Movie(name="Us", description="Adelaide and her family return to "
               + "Adelaide's childhood home and discover that a stranger has  "
               + "been awaiting Adelaide's return.",
               rating="R", score="94", genre=genre3, user=user1)

session.add(movie1)
session.commit()

movie2 = Movie(name="Get Out", description="A man travels with his "
               + "girlfriend to meet her family, but he soon realizes that "
               + "their intentions are quite different from his.",
               rating="R", score="98", genre=genre3, user=user1)

session.add(movie2)
session.commit()

movie3 = Movie(name="The Conjuring", description="A team of paranormal "
               + "investigators are called to help a family who is currently "
               + "dealing with their house's supernatural manifestations.",
               rating="R", score="85", genre=genre3, user=user1)

session.add(movie3)
session.commit()

movie4 = Movie(name="Devil", description="Five strangers in a stuck elevator "
               + "soon realize that one of the occupants is the devil himself "
               + "as he seeks terror on the passengers.",
               rating="PG-13", score="52", genre=genre3, user=user1)

session.add(movie4)
session.commit()

movie5 = Movie(name="Insidious", description="A couple seek the help of a "
               + "demonologist to get their son out of an apparent comatose "
               + "state leaving his body as an open vessel for demons to "
               + "inhabit.",
               rating="PG-13", score="66", genre=genre3, user=user1)

session.add(movie5)
session.commit()

# Movies for action genre
genre4 = Genre(name="Action", user=user1)

session.add(genre4)
session.commit()

movie1 = Movie(name="Jack Reacher", description="An ex-military investigator "
               + "comes back on the grid to help clear the name of an "
               + "ex-military sniper suspected of murdering 5 people.",
               rating="PG-13", score="63", genre=genre4, user=user1)

session.add(movie1)
session.commit()

movie2 = Movie(name="Marvel's Black Panther", description="A scorned relative "
               + "to Wakandan royalty comes to challenge the current Black "
               + "Panther and king of Wakanda for the rights to the throne.",
               rating="PG-13", score="97", genre=genre4, user=user1)

session.add(movie2)
session.commit()

movie3 = Movie(name="The Dark Knight", description="The emergence of The "
               + "Joker in the city of Gotham forces Batman to toe the line "
               + "between heroism and vigilantism.",
               rating="PG-13", score="94", genre=genre4, user=user1)

session.add(movie3)
session.commit()

movie4 = Movie(name="Edge of Tomorrow", description="William Cage is "
               + "mysteriously thrown into a time loop and forced to relive "
               + "the same battle over and over again during a war between "
               + "Earth and a seemingly invincible alien species.",
               rating="PG-13", score="90", genre=genre4, user=user1)

session.add(movie4)
session.commit()

movie5 = Movie(name="Mad Max: Fury Road", description="Furiosa and Mad Max "
               + "escape the tyrant Immortan Joe's desert fortress with the "
               + "tyrant's five wives and lead Immortan Joe and his henchmen "
               + "on a deadly chase through the Wasteland.",
               rating="R", score="97", genre=genre4, user=user1)

session.add(movie5)
session.commit()

# Movies for musical genre
genre5 = Genre(name="Musical", user=user1)

session.add(genre5)
session.commit()

movie1 = Movie(name="Dreamgirls", description="Follow the journey of a "
               + "3-woman singing group as they try to make it to the top of "
               + "the charts and the music world.",
               rating="PG-13", score="78", genre=genre5, user=user1)

session.add(movie1)
session.commit()

movie2 = Movie(name="Into the Woods", description="A baker and his wife meet "
               + "countless fairytale characters as they venture into the "
               + "woods for spell ingredients to deliver to a wicked witch.",
               rating="PG", score="71", genre=genre5, user=user1)

session.add(movie2)
session.commit()

movie3 = Movie(name="Les Miserables", description="A prison officer vows to "
               + "bring a freed criminal, who broke parole, back to prison "
               + "despite the criminal's reinvention of himself and his "
               + "adoption of an orphan.",
               rating="PG-13", score="69", genre=genre5, user=user1)

session.add(movie3)
session.commit()

movie4 = Movie(name="Hairspray", description="An overweight teen becomes an "
               + "overnight celebrity on a popular dance show and fights to "
               + "break normal beauty standards and racial segregation.",
               rating="PG", score="91", genre=genre5, user=user1)

session.add(movie4)
session.commit()

movie5 = Movie(name="La La Land", description="A pianist and an actress fall "
               + "in love but their aspirations threaten to end their "
               + "romance.",
               rating="PG-13", score="91", genre=genre5, user=user1)

session.add(movie5)
session.commit()
