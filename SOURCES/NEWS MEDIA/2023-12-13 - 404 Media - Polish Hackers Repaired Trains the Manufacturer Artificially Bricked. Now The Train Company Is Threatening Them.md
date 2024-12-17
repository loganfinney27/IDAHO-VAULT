---
author:
  - "[[Jason Koebler]]"
outlet:
  - "[[404 Media]]"
URL: https://www.404media.co/polish-hackers-repaired-trains-the-manufacturer-artificially-bricked-now-the-train-company-is-threatening-them/
tags:
  - media/articles
  - 2023/12/13
---
*After breaking [[trains]] simply because an independent repair shop had worked on them, NEWAG is now demanding that [[trains]] fixed by [[hackers]] be removed from service.*

They did [[digital rights management|DRM]] to a [[trains|train]]. 

In one of the coolest and more outrageous repair stories in quite some time, three white-hat [[hackers]] helped a regional [[trains|rail]] company in southwest [[Poland]] unbrick a [[trains|train]] that had been artificially rendered inoperable by the train’s manufacturer after an independent maintenance company worked on it. The train’s manufacturer is now threatening to sue the hackers who were hired by the [[independent repair company]] to fix it. 

The fallout from the situation is currently roiling [[Poland|Polish]] [[infrastructure]] circles and the repair world, with the manufacturer of those trains denying bricking the trains despite ample evidence to the contrary. The manufacturer is also now demanding that the repaired trains immediately be removed from service because they have been “hacked,” and thus might now be unsafe, a claim they also cannot substantiate. 

The situation is a heavy machinery example of something that happens across most categories of electronics, from phones, laptops, health devices, and wearables to tractors and, apparently, trains. In this case, NEWAG, the manufacturer of the Impuls family of trains, put code in the train’s control systems that prevented them from running if a [[Global Positioning System|GPS]] tracker detected that it spent a certain number of days in an [[independent repair company]]’s maintenance center, and also prevented it from running if certain components had been replaced without a manufacturer-approved serial number. 

This anti-repair mechanism is called “parts pairing,” and is a common frustration for farmers who want to repair their John Deere tractors without authorization from the company. It’s also used by Apple to prevent independent repair of iPhones.

In this case, a Polish train operator called Lower Silesian Railway, which operates regional train services from Wrocław, purchased 11 Impuls trains. It began to do regular maintenance on the trains using an independent company called Serwis Pojazdów Szynowych (SPS), which notes on its [[Internet|website]] that “many Polish carriers have trusted us” with train maintenance. Over the course of maintaining four different Impuls trains, SPS found mysterious errors that prevented them from running. SPS became desperate and Googled “Polish hackers” and came across a group called Dragon Sector, a reverse-engineering team made up of white hat hackers. The trains had just undergone “mandatory maintenance” after having traveled a million kilometers.

“This is quite a peculiar part of the story—when SPS was unable to start the trains and almost gave up on their servicing, someone from the workshop typed "polscy hakerzy" (‘Polish hackers’) into Google,” the team from Dragon Sector, made up of Jakub Stępniewicz, Sergiusz Bazański, and Michał Kowalczyk, told me in an email. “Dragon Sector popped up and soon after we received an email asking for help.”

The problem was so bad that an [[infrastructure]] trade publication in Poland called Rynek Kolejowy picked up on the mysterious issues over the summer, and said that the lack of working trains was beginning to impact service: “Four vehicles after level P3-2 repair cannot be started. At this moment, it is not known what caused the failure. The lack of units is a serious problem for the carrier and passengers, because shorter trains are sent on routes.”

The hiring of [[Dragon Sector]] was a last resort: “In 2021, an independent train workshop won a maintenance tender for some trains made by Newag, but it turned out that they didn't start after servicing,” Dragon Sector told me. “[SPS] hired us to analyze the issue and we discovered a ‘workshop-detection’ system built into the train software, which bricked the trains after some conditions were met (two of the trains even used a list of precise [[GPS coordinates]] of competitors' workshops). We also discovered an undocumented ‘unlock code’ which you could enter from the train driver’s panel which magically fixed the issue.”

Dragon Sector was able to bypass the measures and fix the trains. The group posted a [[YouTube]] video of the train operating properly after they’d worked on it.

The news of Dragon Sector’s work was first reported by the [[Poland|Polish]] outlet Zaufana Trzecia Strona and was translated into English by the site Bad Cyber. Kowalczyk and Stępniewicz gave a talk about the saga last week at Poland’s Oh My H@ck conference in Warsaw. The group plans on doing further talks about the technical measures implemented to prevent the trains from running and how they fixed it. 

“These trains were locking up for arbitrary reasons after being serviced at third-party workshops. The manufacturer argued that this was because of malpractice by these workshops, and that they should be serviced by them instead of third parties,” Bazański, who goes by the handle q3k, posted on Mastodon. “After a certain update by NEWAG, the cabin controls would also display scary messages about copyright violations if the human machine interface detected a subset of conditions that should've engaged the lock but the train was still operational. The trains also had a GSM telemetry unit that was broadcasting lock conditions, and in some cases appeared to be able to lock the train remotely.”

All of this has created quite a stir in [[Poland]] (and in repair circles). NEWAG did not respond to a request for comment from 404 Media. But Rynek Kolejowy reported that the company is now very mad, and has threatened to sue the hackers. In a statement to Rynek Kolejowy, NEWAG said “Our software is clean. We have not introduced, we do not introduce and we will not introduce into the software of our trains any solutions that lead to intentional failures. This is slander from our competition, which is conducting an illegal black PR campaign against us.” The company added that it has reported the situation to “the authorized authorities.”

“[[hackers|Hacking]] IT systems is a violation of many legal provisions and a threat to railway traffic safety,” NEWAG added. “We do not know who interfered with the train control software, using what methods and what qualifications. We also notified the Office of Rail Transport about this so that it could decide to withdraw from service the sets subjected to the activities of unknown hackers.”

In response, Dragon Sector released a lengthy statement explaining how they did their work and explaining the types of [[digital rights management|DRM]] they encountered: “We did not interfere with the code of the controllers in Impulsa - all vehicles still run on the original, unmodified software,” part of the statement reads. SPS, meanwhile, has said that its position “is consistent with the position of Dragon Sector.”

Kowalczk told [[404 Media]] that “we are answering media and waiting to be summoned as witnesses,” and added that “NEWAG said that they will sue us, but we doubt they will - their defense line is really poor and they would have no chance defending it, they probably just want to sound scary in the media.” 

This strategy—to intimidate independent repair professionals, claim that the device (in this case, a train) is unsafe, and threaten legal action—is an egregious but common playbook in manufacturers’ fight against repair, all over the world. In the [[United States of America|United States]], an exemption to Section 1201 of the [[Digital Millennium Copyright Act]] allows for repair pros to hack land-based motor vehicles, “which would cover trains,” [[Gay Gordon-Byrne]], executive director of [[right to repair]] advocacy group [[Repair.org]] told [[404 Media]]. 

“All of this is classic [[original equipment manufacturer|OEM]] bullshit,” Gordon-Byrne said, using an acronym for [[original equipment manufacturer]]. “This is the kind of stuff [[digital rights management|DRM]] lets you do, and if you don’t stop it, this is where it goes. What the [[original equipment manufacturer|OEM]] thinks shouldn’t matter anymore, because they’re not the owner of the train anymore. It’s [[digital rights management|DRM]] gone wild.”

But in [[Europe]], the legality of what Dragon Sector did is murkier. Digital rights advocate and [[copyright]] expert [[Cory Doctorow]] explained in his excellent Pluralistic blog that Article 6 of [[Europe]]'s 2001 Copyright and Information Society Directive is generally stricter on [[digital rights management|DRM]] circumvention than Section 1201 of the [[Digital Millennium Copyright Act|DMCA]], and does not have a specific repair exemption. Because of this law, Doctorow told 404 Media that "there is now an extra layer of jeopardy for these researchers. They were brave to come forward and talk about it." Doctorow said that some similar types of research that bypass [[digital rights management|DRM]] and technological protection measures (TPMs) in [[Europe]] has been done anonymously or behind the scenes for this reason, creating a chilling effect on this type of research.

During the height of the [[coronavirus|pandemic]], I wrote an article about how a Polish hacker had developed a dongle that was being used by American repair professionals to bypass [[digital rights management|DRM]] on [[ventilators]] needed to keep [[coronavirus|COVID-19]] patients alive. That hacker wanted to keep themselves anonymous in part because they feared being prosecuted under EU law. Doctorow said that these sorts of cases—ones involving [[tractors]], [[trains]], other things that people obviously should be able to fix, are ones that can help change laws and regulations. "This is the kind of claim that might actually help unravel these anti-circumvention measures," he said. "A Polish [[trains|train]] operator who wants to fix a Polish [[trains|train]] they own is just a no brainer." 

Earlier this week, a group called the [[National Association of Manufacturers]] released a paper called “The Economic Downsides of ‘[[right to repair|Right-to-Repair]]’,” which is nominally a piece of research but is just an astroturfed policy paper for big corporations that oppose repair. The paper includes a section called “Altering equipment poses a dramatic increase in violating safety standards and falling out of federal compliance,” which is an extremely common argument that [[John Deere]], medical device manufacturers, [[Apple]], and many other [[original equipment manufacturer|OEMs]] have made when [[lobbying]] against [[right to repair]] regulations and laws.

In other words, the “safety” line of argument that NEWAG is using to try to undermine this repair is a common refrain across every industry of electronics. 

“You name an industry and I’ll give you an example of something like this,” Gordon-Byrne said. “[[John Deere]] says farm workers are going to die, your tractor is going to run out of control (if repaired without Deere oversight).” She said that the same diagnostic tools that are used to determine what the problem is with a device are “are then run again at the end of the repair, and the diagnostics tell you whether the thing works or not.” In other words, the [[trains|train]] is either fixed, which it appears to be, or it is not.

SPS, NEWAG, and the Lower Silesian Railway did not respond to [[404 Media]]’s requests for comment.

*Update: This article has been updated to include more details about [[Europe]]'s [[copyright laws]].*